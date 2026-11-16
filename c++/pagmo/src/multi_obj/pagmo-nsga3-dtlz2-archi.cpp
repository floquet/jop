/**
 * @file pagmo-nsga3-dtlz2-archi.cpp
 * @brief 3-Objective DTLZ2 Multi-Island TBB Benchmark with Custom C++17 NSGA-III UDA.
 *
 * PROVENANCE & ATTRIBUTION:
 *   [ORIGIN: UPSTREAM - pagmo2 2.19.1]
 *     - `pagmo::dtlz(2, 12, 3)` analytical 3-objective spherical Pareto problem
 *       (Pareto front: f_1^2 + f_2^2 + f_3^2 = 1, f_m >= 0).
 *     - `pagmo::archipelago` & `pagmo::island` TBB parallel execution engine.
 *     - `pagmo::fast_non_dominated_sorting` from `<pagmo/utils/multi_objective.hpp>`.
 *   [ORIGIN: UPSTREAM - Deb & Jain (2014)]
 *     - 3-objective Das-Dennis reference directions (H = 13 => C(15,2) = 105 directions),
 *       ASF extreme-point identification, Eigen FullPivLU hyperplane intercepts,
 *       and niche-preserving survival selection.
 *   [ORIGIN: LOCAL - floquet/jop repo]
 *     - `telemetry::print_provenance(argc, argv)`, Measured vs. Goal verification table,
 *       deterministic per-island seeds, and host-scoped CSV export under logs/<hostname>/.
 *   [ORIGIN: NEW - Written here]
 *     - 24-island parallel execution of `nsga3_uda` on a 3D spherical Pareto surface with
 *       exact radial Generational Distance (GD) and octant anchor verification.
 */

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

#include <unistd.h>
#include <Eigen/Dense>

#include <pagmo/algorithm.hpp>
#include <pagmo/archipelago.hpp>
#include <pagmo/topologies/unconnected.hpp>
#include <pagmo/island.hpp>
#include <pagmo/population.hpp>
#include <pagmo/problem.hpp>
#include <pagmo/problems/dtlz.hpp>
#include <pagmo/utils/multi_objective.hpp>

#include "provenance.hpp"

namespace {

// [ORIGIN: UPSTREAM - Das & Dennis (1998)]
// For M = 3 objectives and H = 13 partitions => C(13 + 3 - 1, 2) = 105 simplex points.
std::vector<std::vector<double>> generate_das_dennis(std::size_t n_obj, std::size_t n_partitions) {
    std::vector<std::vector<double>> refs;
    std::vector<double> current(n_obj, 0.0);

    auto recurse = [&](auto &self, std::size_t obj_idx, std::size_t remaining) -> void {
        if (obj_idx == n_obj - 1) {
            current[obj_idx] = static_cast<double>(remaining) / static_cast<double>(n_partitions);
            refs.push_back(current);
            return;
        }
        for (std::size_t k = 0; k <= remaining; ++k) {
            current[obj_idx] = static_cast<double>(k) / static_cast<double>(n_partitions);
            self(self, obj_idx + 1, remaining - k);
        }
    };

    recurse(recurse, 0, n_partitions);
    return refs;
}

// [ORIGIN: UPSTREAM - Deb & Agrawal (1995)]
std::pair<pagmo::vector_double, pagmo::vector_double> sbx_crossover(
    const pagmo::vector_double &p1,
    const pagmo::vector_double &p2,
    const pagmo::vector_double &lb,
    const pagmo::vector_double &ub,
    double cr,
    double eta_c,
    std::mt19937 &rng) {

    std::uniform_real_distribution<double> uni(0.0, 1.0);
    pagmo::vector_double c1 = p1;
    pagmo::vector_double c2 = p2;
    if (uni(rng) > cr) return {c1, c2};

    for (std::size_t i = 0; i < p1.size(); ++i) {
        if (uni(rng) <= 0.5 && std::abs(p1[i] - p2[i]) > 1e-14) {
            const double y1 = std::min(p1[i], p2[i]);
            const double y2 = std::max(p1[i], p2[i]);
            const double yl = lb[i];
            const double yu = ub[i];
            const double rand_u = uni(rng);

            double beta = 1.0 + (2.0 * (y1 - yl) / (y2 - y1));
            double alpha = 2.0 - std::pow(beta, -(eta_c + 1.0));
            double betaq = (rand_u <= (1.0 / alpha))
                               ? std::pow(rand_u * alpha, 1.0 / (eta_c + 1.0))
                               : std::pow(1.0 / (2.0 - rand_u * alpha), 1.0 / (eta_c + 1.0));
            double child1 = std::clamp(0.5 * ((y1 + y2) - betaq * (y2 - y1)), yl, yu);

            beta = 1.0 + (2.0 * (yu - y2) / (y2 - y1));
            alpha = 2.0 - std::pow(beta, -(eta_c + 1.0));
            betaq = (rand_u <= (1.0 / alpha))
                        ? std::pow(rand_u * alpha, 1.0 / (eta_c + 1.0))
                        : std::pow(1.0 / (2.0 - rand_u * alpha), 1.0 / (eta_c + 1.0));
            double child2 = std::clamp(0.5 * ((y1 + y2) + betaq * (y2 - y1)), yl, yu);

            if (uni(rng) <= 0.5) {
                c1[i] = child2;
                c2[i] = child1;
            } else {
                c1[i] = child1;
                c2[i] = child2;
            }
        }
    }
    return {c1, c2};
}

void polynomial_mutation(
    pagmo::vector_double &x,
    const pagmo::vector_double &lb,
    const pagmo::vector_double &ub,
    double prob_m,
    double eta_m,
    std::mt19937 &rng) {

    std::uniform_real_distribution<double> uni(0.0, 1.0);
    for (std::size_t i = 0; i < x.size(); ++i) {
        if (uni(rng) <= prob_m) {
            const double y = x[i];
            const double yl = lb[i];
            const double yu = ub[i];
            const double delta1 = (y - yl) / (yu - yl);
            const double delta2 = (yu - y) / (yu - yl);
            const double rnd = uni(rng);
            const double mut_pow = 1.0 / (eta_m + 1.0);

            double deltaq = 0.0;
            if (rnd <= 0.5) {
                const double xy = 1.0 - delta1;
                const double val = 2.0 * rnd + (1.0 - 2.0 * rnd) * std::pow(xy, eta_m + 1.0);
                deltaq = std::pow(val, mut_pow) - 1.0;
            } else {
                const double xy = 1.0 - delta2;
                const double val = 2.0 * (1.0 - rnd) + 2.0 * (rnd - 0.5) * std::pow(xy, eta_m + 1.0);
                deltaq = 1.0 - std::pow(val, mut_pow);
            }
            x[i] = std::clamp(y + deltaq * (yu - yl), yl, yu);
        }
    }
}

// [ORIGIN: NEW - Thread-safe C++17 NSGA-III UDA for pagmo::archipelago]
struct nsga3_uda {
    unsigned int gen = 300;
    std::size_t n_partitions = 13;
    double cr = 1.0;
    double eta_c = 30.0;
    double prob_m = 1.0 / 12.0;
    double eta_m = 20.0;
    unsigned int seed = 42;

    nsga3_uda() = default;
    nsga3_uda(unsigned int g, std::size_t part, double crossover_p, double ec,
              double mut_p, double em, unsigned int s)
        : gen(g), n_partitions(part), cr(crossover_p), eta_c(ec),
          prob_m(mut_p), eta_m(em), seed(s) {}

    std::string get_name() const { return "NSGA-III (Deb & Jain 2014 UDA)"; }
    void set_seed(unsigned int s) { seed = s; }

    pagmo::population evolve(pagmo::population pop) const {
        const auto &prob = pop.get_problem();
        const std::size_t n_obj = prob.get_nobj();
        const std::size_t pop_size = pop.size();
        const auto [lb, ub] = prob.get_bounds();
        const auto ref_dirs = generate_das_dennis(n_obj, n_partitions);
        const std::size_t n_refs = ref_dirs.size();

        std::mt19937 rng(seed);
        std::uniform_int_distribution<std::size_t> pick_idx(0, pop_size - 1);

        std::vector<double> z_min(n_obj, std::numeric_limits<double>::infinity());
        for (const auto &f : pop.get_f()) {
            for (std::size_t m = 0; m < n_obj; ++m) z_min[m] = std::min(z_min[m], f[m]);
        }

        for (unsigned int g = 0; g < gen; ++g) {
            std::vector<pagmo::vector_double> combined_x = pop.get_x();
            std::vector<pagmo::vector_double> combined_f = pop.get_f();
            combined_x.reserve(2 * pop_size);
            combined_f.reserve(2 * pop_size);

            while (combined_x.size() < 2 * pop_size) {
                const std::size_t i1 = pick_idx(rng);
                const std::size_t i2 = pick_idx(rng);
                auto [c1, c2] = sbx_crossover(pop.get_x()[i1], pop.get_x()[i2], lb, ub, cr, eta_c, rng);
                polynomial_mutation(c1, lb, ub, prob_m, eta_m, rng);
                polynomial_mutation(c2, lb, ub, prob_m, eta_m, rng);

                auto f1 = prob.fitness(c1);
                for (std::size_t m = 0; m < n_obj; ++m) z_min[m] = std::min(z_min[m], f1[m]);
                combined_x.push_back(std::move(c1));
                combined_f.push_back(std::move(f1));

                if (combined_x.size() < 2 * pop_size) {
                    auto f2 = prob.fitness(c2);
                    for (std::size_t m = 0; m < n_obj; ++m) z_min[m] = std::min(z_min[m], f2[m]);
                    combined_x.push_back(std::move(c2));
                    combined_f.push_back(std::move(f2));
                }
            }

            auto nds = pagmo::fast_non_dominated_sorting(combined_f);
            const auto &fronts = std::get<0>(nds);

            std::vector<std::size_t> next_indices;
            next_indices.reserve(pop_size);
            std::size_t last_front_idx = 0;

            for (std::size_t f_idx = 0; f_idx < fronts.size(); ++f_idx) {
                if (next_indices.size() + fronts[f_idx].size() <= pop_size) {
                    for (auto idx : fronts[f_idx]) next_indices.push_back(idx);
                    if (next_indices.size() == pop_size) {
                        last_front_idx = f_idx;
                        break;
                    }
                } else {
                    last_front_idx = f_idx;
                    break;
                }
            }

            if (next_indices.size() < pop_size) {
                const std::size_t k_needed = pop_size - next_indices.size();
                const auto &fl = fronts[last_front_idx];

                std::vector<std::size_t> st_indices = next_indices;
                st_indices.insert(st_indices.end(), fl.begin(), fl.end());
                const std::size_t st_size = st_indices.size();

                Eigen::MatrixXd f_prime(st_size, n_obj);
                for (std::size_t i = 0; i < st_size; ++i) {
                    for (std::size_t m = 0; m < n_obj; ++m) {
                        f_prime(i, m) = combined_f[st_indices[i]][m] - z_min[m];
                    }
                }

                Eigen::MatrixXd extreme_pts(n_obj, n_obj);
                for (std::size_t j = 0; j < n_obj; ++j) {
                    double best_asf = std::numeric_limits<double>::infinity();
                    std::size_t best_i = 0;
                    for (std::size_t i = 0; i < st_size; ++i) {
                        double max_ratio = 0.0;
                        for (std::size_t m = 0; m < n_obj; ++m) {
                            const double w = (m == j) ? 1.0 : 1e-6;
                            max_ratio = std::max(max_ratio, f_prime(i, m) / w);
                        }
                        if (max_ratio < best_asf) {
                            best_asf = max_ratio;
                            best_i = i;
                        }
                    }
                    extreme_pts.row(j) = f_prime.row(best_i);
                }

                Eigen::VectorXd intercepts(n_obj);
                Eigen::FullPivLU<Eigen::MatrixXd> lu(extreme_pts);
                bool valid_plane = false;
                if (lu.isInvertible()) {
                    Eigen::VectorXd u = lu.solve(Eigen::VectorXd::Ones(n_obj));
                    if ((u.array() > 1e-12).all()) {
                        intercepts = u.cwiseInverse();
                        valid_plane = true;
                    }
                }
                if (!valid_plane) {
                    for (std::size_t m = 0; m < n_obj; ++m) {
                        intercepts(m) = std::max(1e-12, f_prime.col(m).maxCoeff());
                    }
                }

                Eigen::MatrixXd f_norm = f_prime.array().rowwise() / intercepts.transpose().array();

                std::vector<std::size_t> assoc_ref(st_size, 0);
                std::vector<double> perp_dist(st_size, std::numeric_limits<double>::infinity());

                for (std::size_t i = 0; i < st_size; ++i) {
                    const Eigen::VectorXd s = f_norm.row(i);
                    for (std::size_t r = 0; r < n_refs; ++r) {
                        Eigen::Map<const Eigen::VectorXd> w(ref_dirs[r].data(), n_obj);
                        const double w_norm = w.norm();
                        const double proj = s.dot(w) / w_norm;
                        const Eigen::VectorXd perp = s - (proj / w_norm) * w;
                        const double d = perp.norm();
                        if (d < perp_dist[i]) {
                            perp_dist[i] = d;
                            assoc_ref[i] = r;
                        }
                    }
                }

                const std::size_t already_selected = next_indices.size();
                std::vector<std::size_t> rho(n_refs, 0);
                for (std::size_t i = 0; i < already_selected; ++i) rho[assoc_ref[i]]++;

                std::vector<std::vector<std::size_t>> fl_members(n_refs);
                for (std::size_t i = already_selected; i < st_size; ++i) {
                    fl_members[assoc_ref[i]].push_back(i);
                }

                std::vector<bool> ref_excluded(n_refs, false);
                std::size_t added = 0;

                while (added < k_needed) {
                    std::size_t min_rho = std::numeric_limits<std::size_t>::max();
                    for (std::size_t r = 0; r < n_refs; ++r) {
                        if (!ref_excluded[r]) min_rho = std::min(min_rho, rho[r]);
                    }

                    std::vector<std::size_t> min_refs;
                    for (std::size_t r = 0; r < n_refs; ++r) {
                        if (!ref_excluded[r] && rho[r] == min_rho) min_refs.push_back(r);
                    }

                    std::uniform_int_distribution<std::size_t> pick_ref(0, min_refs.size() - 1);
                    const std::size_t chosen_r = min_refs[pick_ref(rng)];

                    if (fl_members[chosen_r].empty()) {
                        ref_excluded[chosen_r] = true;
                        continue;
                    }

                    std::size_t chosen_pos = 0;
                    if (rho[chosen_r] == 0) {
                        double best_d = std::numeric_limits<double>::infinity();
                        for (std::size_t pos = 0; pos < fl_members[chosen_r].size(); ++pos) {
                            const std::size_t member_i = fl_members[chosen_r][pos];
                            if (perp_dist[member_i] < best_d) {
                                best_d = perp_dist[member_i];
                                chosen_pos = pos;
                            }
                        }
                    } else {
                        std::uniform_int_distribution<std::size_t> pick_m(0, fl_members[chosen_r].size() - 1);
                        chosen_pos = pick_m(rng);
                    }

                    const std::size_t chosen_st_i = fl_members[chosen_r][chosen_pos];
                    next_indices.push_back(st_indices[chosen_st_i]);
                    fl_members[chosen_r].erase(fl_members[chosen_r].begin() + chosen_pos);
                    rho[chosen_r]++;
                    added++;
                }
            }

            pagmo::population next_pop{prob};
            for (auto idx : next_indices) next_pop.push_back(combined_x[idx], combined_f[idx]);
            pop = std::move(next_pop);
        }

        return pop;
    }
};

// [ORIGIN: NEW - Analytical spherical Pareto surface check: ||f||_2 == 1.0]
struct Dtlz2Metrics {
    double radial_gd;
    double max_radial_err;
    double max_f1;
    double max_f2;
    double max_f3;
    std::size_t nd_count;
    unsigned long long fevals;
};

Dtlz2Metrics evaluate_dtlz2_sphere(const pagmo::population &pop) {
    const auto &f_vecs = pop.get_f();
    const auto nds = pagmo::fast_non_dominated_sorting(f_vecs);
    const auto &rank0 = std::get<0>(nds)[0];

    double sum_sq = 0.0;
    double max_err = 0.0;
    double m1 = 0.0, m2 = 0.0, m3 = 0.0;

    for (auto idx : rank0) {
        const double f1 = f_vecs[idx][0];
        const double f2 = f_vecs[idx][1];
        const double f3 = f_vecs[idx][2];
        const double r = std::sqrt(f1 * f1 + f2 * f2 + f3 * f3);
        const double err = std::abs(r - 1.0);
        sum_sq += err * err;
        max_err = std::max(max_err, err);
        m1 = std::max(m1, f1);
        m2 = std::max(m2, f2);
        m3 = std::max(m3, f3);
    }

    const double gd = rank0.empty() ? 1e30 : std::sqrt(sum_sq) / static_cast<double>(rank0.size());
    return {gd, max_err, m1, m2, m3, rank0.size(), pop.get_problem().get_fevals()};
}

} // namespace

int main(int argc, char **argv) {
    try {
        constexpr unsigned int prob_id = 2;       // DTLZ2 (unit sphere Pareto surface)
        constexpr pagmo::vector_double::size_type dim = 12;
        constexpr pagmo::vector_double::size_type n_obj = 3;
        constexpr std::size_t n_partitions = 13;  // C(13+3-1, 2) = 105 reference directions
        constexpr std::size_t pop_size = 108;     // Multiple of 4 >= 105 reference points
        constexpr unsigned int generations = 300;
        constexpr double cr = 1.0;
        constexpr double eta_c = 30.0;
        constexpr double prob_m = 1.0 / static_cast<double>(dim);
        constexpr double eta_m = 20.0;
        constexpr unsigned int base_seed = 42;

        const std::size_t n_islands = std::max(1u, std::thread::hardware_concurrency());
        constexpr double goal_gd = 1.0e-3;
        constexpr double goal_anchor = 0.98;

        std::cout << "========================================================================================\n"
                  << "PAGMO2 3-OBJECTIVE DTLZ2 + 24-ISLAND TBB NSGA-III BENCHMARK INTENT & EXPECTED OUTCOME\n"
                  << "========================================================================================\n"
                  << "Problem:    DTLZ2 (D = " << dim << ", M = " << n_obj << ", analytical f1^2 + f2^2 + f3^2 = 1)\n"
                  << "Algorithm:  nsga3_uda (pop=" << pop_size << ", ref_dirs=105 [H=" << n_partitions
                  << "], gens=" << generations << ", cr=" << cr << ", eta_c=" << eta_c << ", eta_m=" << eta_m << ")\n"
                  << "Topology:   " << n_islands << " parallel islands (Intel oneTBB backend)\n"
                  << "Goal:       Radial GD < " << std::scientific << std::setprecision(2) << goal_gd
                  << ", ND_Pts >= 100, Axis Anchors max(f_m) > " << std::fixed << goal_anchor << "\n\n";

        pagmo::problem prob{pagmo::dtlz(prob_id, dim, n_obj)};
        pagmo::archipelago archi{pagmo::unconnected{}};

        for (std::size_t i = 0; i < n_islands; ++i) {
            nsga3_uda uda{generations, n_partitions, cr, eta_c, prob_m, eta_m,
                          base_seed + static_cast<unsigned int>(i)};
            pagmo::algorithm algo{uda};
            pagmo::population pop{prob, pop_size, base_seed + 1000u + static_cast<unsigned int>(i)};
            archi.push_back(pagmo::island{algo, pop});
        }

        const auto t0 = std::chrono::steady_clock::now();
        archi.evolve(1);
        archi.wait_check();
        const auto t1 = std::chrono::steady_clock::now();
        const double elapsed_s = std::chrono::duration<double>(t1 - t0).count();

        std::cout << "========================================================================================\n"
                  << "ISLAND 3D SPHERICAL PARETO VERIFICATION (MEASURED VS. GOAL)\n"
                  << "========================================================================================\n"
                  << "Island  ND_Pts  Radial_GD     Max_Rad_Err   max(f1, f2, f3)           Fevals   Status\n"
                  << "----------------------------------------------------------------------------------------\n";

        bool all_pass = true;
        unsigned long long total_fevals = 0;

        for (std::size_t i = 0; i < n_islands; ++i) {
            const auto pop = archi[i].get_population();
            const auto m = evaluate_dtlz2_sphere(pop);
            total_fevals += m.fevals;

            const bool pass = (m.radial_gd < goal_gd) &&
                              (m.nd_count >= 100) &&
                              (m.max_f1 > goal_anchor) &&
                              (m.max_f2 > goal_anchor) &&
                              (m.max_f3 > goal_anchor);
            all_pass = all_pass && pass;

            std::cout << std::left << std::setw(8) << i
                      << std::setw(8) << m.nd_count
                      << std::scientific << std::setprecision(4)
                      << std::setw(14) << m.radial_gd
                      << std::setw(14) << m.max_radial_err
                      << std::fixed << std::setprecision(3)
                      << "(" << m.max_f1 << ", " << m.max_f2 << ", " << m.max_f3 << ")   "
                      << std::setw(9) << m.fevals
                      << (pass ? "PASS" : "FAIL") << "\n";
        }

        // Export Island 0 3D Pareto front to logs/<hostname>/
        char host_buf[256] = "unknown";
        gethostname(host_buf, sizeof(host_buf));
        std::ofstream csv("logs/" + std::string(host_buf) + "/pagmo-nsga3-dtlz2_front_" + std::string(host_buf) + ".csv");
        if (csv) {
            csv << "f1,f2,f3,radius\n";
            const auto pop0 = archi[0].get_population();
            for (const auto &f : pop0.get_f()) {
                const double r = std::sqrt(f[0] * f[0] + f[1] * f[1] + f[2] * f[2]);
                csv << std::setprecision(12) << f[0] << "," << f[1] << "," << f[2] << "," << r << "\n";
            }
        }

        const double kevals_s = (static_cast<double>(total_fevals) / elapsed_s) / 1.0e3;
        std::cout << "----------------------------------------------------------------------------------------\n"
                  << "Wall-Clock Time:      " << std::fixed << std::setprecision(4) << elapsed_s << " s\n"
                  << "Total Fevals:         " << total_fevals << " (" << std::setprecision(1) << kevals_s << " k evals/sec)\n"
                  << "Overall Verification: " << (all_pass ? "SUCCESS" : "FAILURE") << "\n\n";

        telemetry::print_provenance(argc, argv);
        return all_pass ? EXIT_SUCCESS : EXIT_FAILURE;

    } catch (const std::exception &e) {
        std::cerr << "An error occurred: " << e.what() << '\n';
        return EXIT_FAILURE;
    }
}
