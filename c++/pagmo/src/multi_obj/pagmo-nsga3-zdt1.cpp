/**
 * @file pagmo-nsga3-zdt1.cpp
 * @brief True NSGA-III (Deb & Jain 2014) User-Defined Algorithm (UDA) in pagmo2 on ZDT1,
 *        parameter-locked to pymoo's NSGA3 for cross-language parity verification.
 *
 * PROVENANCE & ATTRIBUTION:
 *   [ORIGIN: UPSTREAM - pagmo2 2.19.1]
 *     - Problem instantiation `pagmo::zdt(1, 30)` and `pagmo::population` / `pagmo::algorithm`
 *       type-erasure interface (evolve(population) const, get_name(), set_seed()).
 *     - Fast non-dominated sorting (`pagmo::fast_non_dominated_sorting`) and hypervolume/front
 *       utilities from `<pagmo/utils/multi_objective.hpp>`.
 *     - SBX crossover & polynomial mutation formulas matching Deb & Agrawal (1995) /
 *       pagmo2's `sbx_crossover` and `polynomial_mutation` conventions.
 *   [ORIGIN: UPSTREAM - Deb & Jain (2014) / pymoo NSGA3]
 *     - Das & Dennis (1998) structured reference directions on the unit simplex.
 *     - Ideal-point translation, ASF extreme-point identification, hyperplane intercept
 *       normalization, perpendicular Euclidean distance association, and niche-preserving
 *       survival selection (Algorithm 1-4, IEEE TEVC 18(4):577-601, 2014).
 *   [ORIGIN: LOCAL - floquet/jop repo]
 *     - `provenance.hpp` telemetry header (`print_system_telemetry()`), Measured vs. Goal
 *       verification table, deterministic seed (`42`), and exit-code contract (`0`/`1`).
 *   [ORIGIN: NEW - Written here]
 *     - Complete C++17 `nsga3_uda` struct implementing Deb & Jain (2014) survival selection
 *       inside `pagmo2` (which natively ships `nsga2` and `moead`, not `nsga3`), plus exact
 *       Generational Distance (GD) and Inverse Generational Distance (IGD) parity checks.
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
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

#include <Eigen/Dense>
#include <pagmo/algorithm.hpp>
#include <pagmo/population.hpp>
#include <pagmo/problem.hpp>
#include <pagmo/problems/zdt.hpp>
#include <pagmo/utils/multi_objective.hpp>

#include "provenance.hpp"

namespace {

// =============================================================================
// [ORIGIN: UPSTREAM - Das & Dennis (1998) / pymoo get_reference_directions("das-dennis")]
// Generate uniform reference points on the M-objective unit simplex with H partitions.
// Count = C(H + M - 1, M - 1). For M = 2, H = 99 => 100 evenly spaced points.
// =============================================================================
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

// =============================================================================
// [ORIGIN: UPSTREAM - Deb & Agrawal (1995) / pagmo2 SBX + Polynomial Mutation]
// Bounded Simulated Binary Crossover (SBX) and Polynomial Mutation matching pymoo/pagmo2.
// =============================================================================
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

    if (uni(rng) > cr) {
        return {c1, c2};
    }

    const std::size_t dim = p1.size();
    for (std::size_t i = 0; i < dim; ++i) {
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
            double child1 = 0.5 * ((y1 + y2) - betaq * (y2 - y1));

            beta = 1.0 + (2.0 * (yu - y2) / (y2 - y1));
            alpha = 2.0 - std::pow(beta, -(eta_c + 1.0));
            betaq = (rand_u <= (1.0 / alpha))
                        ? std::pow(rand_u * alpha, 1.0 / (eta_c + 1.0))
                        : std::pow(1.0 / (2.0 - rand_u * alpha), 1.0 / (eta_c + 1.0));
            double child2 = 0.5 * ((y1 + y2) + betaq * (y2 - y1));

            child1 = std::clamp(child1, yl, yu);
            child2 = std::clamp(child2, yl, yu);

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

// =============================================================================
// [ORIGIN: NEW - Written here, implementing Deb & Jain (2014) Algorithms 1-4]
// Custom pagmo2 User-Defined Algorithm (UDA) for NSGA-III.
// Satisfies pagmo::algorithm concept: evolve(population), get_name(), set_seed().
// =============================================================================
struct nsga3_uda {
    unsigned int gen = 250;
    std::size_t n_partitions = 99;
    double cr = 0.95;
    double eta_c = 10.0;
    double prob_m = 0.01;
    double eta_m = 50.0;
    unsigned int seed = 42;
    unsigned int verbosity = 0;

    nsga3_uda() = default;
    nsga3_uda(unsigned int g, std::size_t part, double crossover_p, double ec,
              double mut_p, double em, unsigned int s)
        : gen(g), n_partitions(part), cr(crossover_p), eta_c(ec),
          prob_m(mut_p), eta_m(em), seed(s) {}

    std::string get_name() const { return "NSGA-III (Deb & Jain 2014 UDA)"; }
    void set_seed(unsigned int s) { seed = s; }
    void set_verbosity(unsigned int level) { verbosity = level; }

    pagmo::population evolve(pagmo::population pop) const {
        const auto &prob = pop.get_problem();
        const std::size_t n_obj = prob.get_nobj();
        const std::size_t pop_size = pop.size();
        if (n_obj < 2) {
            throw std::invalid_argument("NSGA-III requires at least 2 objectives.");
        }

        const auto [lb, ub] = prob.get_bounds();
        const auto ref_dirs = generate_das_dennis(n_obj, n_partitions);
        const std::size_t n_refs = ref_dirs.size();

        std::mt19937 rng(seed);
        std::uniform_int_distribution<std::size_t> pick_idx(0, pop_size - 1);

        // Ideal point z_min tracked monotonically across all evaluated individuals
        std::vector<double> z_min(n_obj, std::numeric_limits<double>::infinity());
        for (const auto &f : pop.get_f()) {
            for (std::size_t m = 0; m < n_obj; ++m) {
                z_min[m] = std::min(z_min[m], f[m]);
            }
        }

        for (unsigned int g = 0; g < gen; ++g) {
            // 1. Generate N offspring via random-parent SBX + Polynomial Mutation
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

            // 2. Non-dominated sorting on R_t (size 2N) using pagmo2 built-in routine
            auto nds = pagmo::fast_non_dominated_sorting(combined_f);
            const auto &fronts = std::get<0>(nds);

            std::vector<std::size_t> next_indices;
            next_indices.reserve(pop_size);
            std::size_t last_front_idx = 0;

            for (std::size_t f_idx = 0; f_idx < fronts.size(); ++f_idx) {
                if (next_indices.size() + fronts[f_idx].size() <= pop_size) {
                    for (auto idx : fronts[f_idx]) {
                        next_indices.push_back(idx);
                    }
                    if (next_indices.size() == pop_size) {
                        last_front_idx = f_idx;
                        break;
                    }
                } else {
                    last_front_idx = f_idx;
                    break;
                }
            }

            // 3. Deb & Jain (2014) Reference-Point Niching on Splitting Front F_l
            if (next_indices.size() < pop_size) {
                const std::size_t k_needed = pop_size - next_indices.size();
                const auto &fl = fronts[last_front_idx];

                std::vector<std::size_t> st_indices = next_indices;
                st_indices.insert(st_indices.end(), fl.begin(), fl.end());
                const std::size_t st_size = st_indices.size();

                // 3a. Translate objectives: f'_i = f_i - z_min
                Eigen::MatrixXd f_prime(st_size, n_obj);
                for (std::size_t i = 0; i < st_size; ++i) {
                    for (std::size_t m = 0; m < n_obj; ++m) {
                        f_prime(i, m) = combined_f[st_indices[i]][m] - z_min[m];
                    }
                }

                // 3b. Extreme points via Achievement Scalarizing Function (ASF)
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

                // 3c. Hyperplane intercepts a_m (fallback to max f' if singular)
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

                // Normalize f^n(i, m) = f'(i, m) / intercepts(m)
                Eigen::MatrixXd f_norm = f_prime.array().rowwise() / intercepts.transpose().array();

                // 3d. Associate every member of S_t with nearest reference line (perpendicular dist)
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

                // 3e. Niche count rho_j from already-selected fronts F_1..F_{l-1}
                const std::size_t already_selected = next_indices.size();
                std::vector<std::size_t> rho(n_refs, 0);
                for (std::size_t i = 0; i < already_selected; ++i) {
                    rho[assoc_ref[i]]++;
                }

                // Group F_l members (indices [already_selected .. st_size - 1]) by reference dir
                std::vector<std::vector<std::size_t>> fl_members(n_refs);
                for (std::size_t i = already_selected; i < st_size; ++i) {
                    fl_members[assoc_ref[i]].push_back(i);
                }

                std::vector<bool> ref_excluded(n_refs, false);
                std::size_t added = 0;

                while (added < k_needed) {
                    // Find minimum niche count among active reference directions
                    std::size_t min_rho = std::numeric_limits<std::size_t>::max();
                    for (std::size_t r = 0; r < n_refs; ++r) {
                        if (!ref_excluded[r]) {
                            min_rho = std::min(min_rho, rho[r]);
                        }
                    }

                    std::vector<std::size_t> min_refs;
                    for (std::size_t r = 0; r < n_refs; ++r) {
                        if (!ref_excluded[r] && rho[r] == min_rho) {
                            min_refs.push_back(r);
                        }
                    }

                    std::uniform_int_distribution<std::size_t> pick_ref(0, min_refs.size() - 1);
                    const std::size_t chosen_r = min_refs[pick_ref(rng)];

                    if (fl_members[chosen_r].empty()) {
                        ref_excluded[chosen_r] = true;
                        continue;
                    }

                    // If rho == 0, pick minimum perpendicular distance; else pick randomly
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

            // 4. Write selected N individuals back into pagmo::population
            pagmo::population next_pop{prob};
            for (auto idx : next_indices) {
                next_pop.push_back(combined_x[idx], combined_f[idx]);
            }
            pop = std::move(next_pop);

            if (verbosity > 0 && ((g + 1) % verbosity == 0 || g == 0)) {
                std::cout << "Gen " << std::setw(4) << (g + 1)
                          << " | Fevals: " << std::setw(7) << pop.get_problem().get_fevals()
                          << " | z_min: [" << std::scientific << std::setprecision(4)
                          << z_min[0] << ", " << z_min[1] << "]\n";
            }
        }

        return pop;
    }
};

// =============================================================================
// [ORIGIN: NEW - Written here]
// Compute exact Generational Distance (GD) and Inverted Generational Distance (IGD)
// against the analytical ZDT1 Pareto front f2 = 1 - sqrt(f1), f1 in [0, 1].
// =============================================================================
struct FrontMetrics {
    double gd;
    double igd;
    double f1_min;
    double f1_max;
    std::size_t nd_count;
};

FrontMetrics compute_zdt1_metrics(const pagmo::population &pop) {
    const auto &f_vecs = pop.get_f();
    const auto nd_idx = pagmo::non_dominated_front_2d(f_vecs);

    // 1. GD: distance from each obtained non-dominated solution to analytical curve
    double gd_sum_sq = 0.0;
    double f1_min = 1e30;
    double f1_max = -1e30;

    for (auto idx : nd_idx) {
        const double f1 = f_vecs[idx][0];
        const double f2 = f_vecs[idx][1];
        const double f2_exact = 1.0 - std::sqrt(std::max(0.0, f1));
        const double err = std::abs(f2 - f2_exact);
        gd_sum_sq += err * err;
        f1_min = std::min(f1_min, f1);
        f1_max = std::max(f1_max, f1);
    }
    const double gd = nd_idx.empty() ? 1e30 : std::sqrt(gd_sum_sq) / static_cast<double>(nd_idx.size());

    // 2. IGD: distance from 500 uniform true Pareto points to nearest obtained ND point
    constexpr std::size_t n_ref = 500;
    double igd_sum = 0.0;
    for (std::size_t k = 0; k < n_ref; ++k) {
        const double t1 = static_cast<double>(k) / static_cast<double>(n_ref - 1);
        const double t2 = 1.0 - std::sqrt(t1);
        double min_d = std::numeric_limits<double>::infinity();
        for (auto idx : nd_idx) {
            const double df1 = f_vecs[idx][0] - t1;
            const double df2 = f_vecs[idx][1] - t2;
            min_d = std::min(min_d, std::hypot(df1, df2));
        }
        igd_sum += min_d;
    }
    const double igd = igd_sum / static_cast<double>(n_ref);

    return {gd, igd, f1_min, f1_max, nd_idx.size()};
}

} // namespace

int main(int argc, char **argv) {
    try {
        // [ORIGIN: LOCAL] Parameter-locked to python/pymoo-nsga3-zdt1.py
        constexpr unsigned int prob_id = 1;       // ZDT1
        constexpr pagmo::vector_double::size_type dim = 30;
        constexpr std::size_t pop_size = 100;
        constexpr std::size_t n_partitions = 99;  // 100 Das-Dennis reference directions
        constexpr unsigned int generations = 250;
        constexpr double cr = 0.95;
        constexpr double eta_c = 10.0;
        constexpr double prob_m = 0.01;
        constexpr double eta_m = 50.0;
        constexpr unsigned int seed = 42;

        // Pass/Fail Verification Goals
        constexpr double goal_gd = 1.0e-3;
        constexpr double goal_igd = 1.5e-2;

        std::cout << "========================================================================================\n"
                  << "PAGMO2 TRUE NSGA-III BENCHMARK INTENT & EXPECTED OUTCOME (ZDT1)\n"
                  << "========================================================================================\n"
                  << "Problem:    ZDT1 (D = " << dim << ", 2 objectives, analytical f2 = 1 - sqrt(f1))\n"
                  << "Algorithm:  nsga3_uda (pop=" << pop_size << ", ref_dirs=" << (n_partitions + 1)
                  << ", gens=" << generations << ", cr=" << cr << ", eta_c=" << eta_c
                  << ", prob_m=" << prob_m << ", eta_m=" << eta_m << ", seed=" << seed << ")\n"
                  << "Goal:       GD < " << std::scientific << std::setprecision(2) << goal_gd
                  << ", IGD < " << goal_igd << ", ND_Count >= 95\n\n";

        pagmo::problem prob{pagmo::zdt(prob_id, dim)};
        nsga3_uda uda{generations, n_partitions, cr, eta_c, prob_m, eta_m, seed};
        uda.set_verbosity(50);

        pagmo::algorithm algo{uda};
        pagmo::population pop{prob, pop_size, seed};

        const auto t0 = std::chrono::steady_clock::now();
        pop = algo.evolve(pop);
        const auto t1 = std::chrono::steady_clock::now();
        const double elapsed_s = std::chrono::duration<double>(t1 - t0).count();

        const auto metrics = compute_zdt1_metrics(pop);
        const bool pass = (metrics.gd < goal_gd) &&
                          (metrics.igd < goal_igd) &&
                          (metrics.nd_count >= 95);

        std::cout << "\n========================================================================================\n"
                  << "PAGMO2 NSGA-III RESULTS SUMMARY (MEASURED VS. GOAL)\n"
                  << "========================================================================================\n"
                  << "Metric                Measured        Goal            Status\n"
                  << "----------------------------------------------------------------------------------------\n"
                  << "Non-Dominated Pts     " << std::setw(16) << std::left << metrics.nd_count
                  << std::setw(16) << ">= 95" << (metrics.nd_count >= 95 ? "PASS" : "FAIL") << "\n"
                  << std::scientific << std::setprecision(4)
                  << "Generational Dist(GD) " << std::setw(16) << metrics.gd
                  << std::setw(16) << "< 1.0000e-03" << (metrics.gd < goal_gd ? "PASS" : "FAIL") << "\n"
                  << "Inverted GD (IGD)     " << std::setw(16) << metrics.igd
                  << std::setw(16) << "< 1.5000e-02" << (metrics.igd < goal_igd ? "PASS" : "FAIL") << "\n"
                  << std::fixed << std::setprecision(6)
                  << "f1 Range              [" << metrics.f1_min << ", " << metrics.f1_max << "]\n"
                  << "Total Fevals          " << pop.get_problem().get_fevals() << "\n"
                  << "Wall-Clock Time       " << std::setprecision(4) << elapsed_s << " s\n"
                  << "Overall Verification: " << (pass ? "SUCCESS" : "FAILURE") << "\n";

        // Export Pareto front CSV for side-by-side comparison with pymoo
        char host_buf[256] = "unknown";
        gethostname(host_buf, sizeof(host_buf));
        std::ofstream csv("logs/" + std::string(host_buf) + "/pagmo-nsga3-zdt1_front_" + std::string(host_buf) + ".csv");
        if (csv) {
            csv << "f1,f2\n";
            for (const auto &f : pop.get_f()) {
                csv << std::setprecision(12) << f[0] << "," << f[1] << "\n";
            }
        }

        std::cout << "\n"; telemetry::print_provenance(argc, argv);
        return pass ? EXIT_SUCCESS : EXIT_FAILURE;

    } catch (const std::exception &e) {
        std::cerr << "An error occurred: " << e.what() << '\n';
        return EXIT_FAILURE;
    }
}
