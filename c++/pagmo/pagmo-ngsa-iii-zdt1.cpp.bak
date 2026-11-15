#include <iostream>
#include <pagmo/problem.hpp>
#include <pagmo/problems/zdt.hpp>
#include <pagmo/algorithm.hpp>
#include <pagmo/algorithms/nsga3.hpp>
#include <pagmo/population.hpp>

int main() {
    try {
        // 1. Define the ZDT1 problem (prob_id = 1, dimension = 30)
        pagmo::problem prob{pagmo::zdt(1, 30)};

        // 2. Instantiate the NSGA-III algorithm 
        // Parameters: generations = 250, seed = 42
        pagmo::algorithm algo{pagmo::nsga3(250, 42)};

        // Set verbosity to track progress every 10 generations
        algo.set_verbosity(10);

        // 3. Create a population of size 100
        pagmo::population pop{prob, 100, 42};

        std::cout << "Starting optimization with NSGA-III on ZDT1...\n";

        // 4. Evolve the population
        pop = algo.evolve(pop);

        // 5. Extract results
        const auto& fits = pop.get_f();  // Objective values
        const auto& vectors = pop.get_x(); // Decision variables

        std::cout << "\nOptimization finished!\n";
        std::cout << "Final population size: " << pop.size() << "\n";
        std::cout << "Number of objectives: " << prob.get_nobj() << "\n";

    } catch (const std::exception& e) {
        std::cerr << "An error occurred: " << e.what() << '\n';
        return 1;
    }

    return 0;
}