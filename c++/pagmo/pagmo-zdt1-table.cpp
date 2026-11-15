#include <cmath>
#include <iomanip>
#include <iostream>
#include <pagmo/algorithm.hpp>
#include <pagmo/algorithms/nsga2.hpp>
#include <pagmo/population.hpp>
#include <pagmo/problem.hpp>
#include <pagmo/problems/zdt.hpp>
#include <pagmo/utils/multi_objective.hpp>

int main() {
    pagmo::problem prob{pagmo::zdt{1, 30}};
    pagmo::population pop{prob, 100, 42};
    pagmo::algorithm algo{pagmo::nsga2{10, 0.95, 10., 0.01, 50., 42}};

    const double goal1 = 0.0;
    const double goal2 = 0.0;

    std::cout << std::left
              << std::setw(8)  << "Gen"
              << std::setw(10) << "Fevals"
              << std::setw(15) << "f1_Meas"
              << std::setw(10) << "f1_Goal"
              << std::setw(15) << "f1_Diff"
              << std::setw(15) << "f2_Meas"
              << std::setw(10) << "f2_Goal"
              << std::setw(15) << "f2_Diff"
              << std::setw(15) << "L2_Dist" << "\n";
    std::cout << std::string(113, '-') << "\n";

    std::cout << std::scientific << std::setprecision(5);
    for (int step = 0; step <= 25; ++step) {
        if (step > 0) {
            pop = algo.evolve(pop);
        }
        auto ideal = pagmo::ideal(pop.get_f());
        double diff1 = ideal[0] - goal1;
        double diff2 = ideal[1] - goal2;
        double dist  = std::hypot(diff1, diff2);

        std::cout << std::left
                  << std::setw(8)  << (step * 10)
                  << std::setw(10) << pop.get_problem().get_fevals()
                  << std::setw(15) << ideal[0]
                  << std::setw(10) << std::defaultfloat << goal1 << std::scientific
                  << std::setw(15) << std::showpos << diff1 << std::noshowpos
                  << std::setw(15) << ideal[1]
                  << std::setw(10) << std::defaultfloat << goal2 << std::scientific
                  << std::setw(15) << std::showpos << diff2 << std::noshowpos
                  << std::setw(15) << dist << "\n";
    }
    return 0;
}
