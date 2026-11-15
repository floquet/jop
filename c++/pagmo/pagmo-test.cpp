#include <cmath>
#include <filesystem>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <string>
#include <thread>
#include <vector>
#include <sys/utsname.h>
#include <unistd.h>

#include <pagmo/algorithm.hpp>
#include <pagmo/algorithms/de.hpp>
#include <pagmo/archipelago.hpp>
#include <pagmo/config.hpp>
#include <pagmo/problem.hpp>
#include <pagmo/problems/rosenbrock.hpp>

std::string get_compiler_info() {
#if defined(__clang__)
    return "Clang " + std::string(__clang_version__);
#elif defined(__GNUC__)
    return "GCC " + std::to_string(__GNUC__) + "." + std::to_string(__GNUC_MINOR__) + "." + std::to_string(__GNUC_PATCHLEVEL__);
#else
    return "Unknown C++ Compiler";
#endif
}

std::string get_build_flags() {
    std::string flags;
#ifdef NDEBUG
    flags += "Release (-DNDEBUG) ";
#else
    flags += "Debug ";
#endif
#ifdef __OPTIMIZE__
    flags += "[Optimized] ";
#endif
#ifdef __FAST_MATH__
    flags += "[-ffast-math] ";
#endif
    return flags.empty() ? "Default" : flags;
}

int main(int argc, char* argv[]) {
    // --- 1. Gather Portable System & Build Information ---
    struct utsname sys_info {};
    uname(&sys_info);

    char hostname[256] = "unknown";
    gethostname(hostname, sizeof(hostname));

    const std::string cwd = std::filesystem::current_path().string();
    const unsigned int hw_threads = std::thread::hardware_concurrency();

    std::cout << "================================================================================\n";
    std::cout << "SYSTEM & BUILD TELEMETRY\n";
    std::cout << "================================================================================\n";
    std::cout << std::left
              << std::setw(22) << "Host:"          << hostname << "\n"
              << std::setw(22) << "OS / Kernel:"   << sys_info.sysname << " " << sys_info.release << " (" << sys_info.machine << ")\n"
              << std::setw(22) << "Hardware Threads:" << hw_threads << "\n"
              << std::setw(22) << "Working Dir:"   << cwd << "\n"
              << std::setw(22) << "Executable:"    << (argc > 0 ? argv[0] : "unknown") << "\n"
              << std::setw(22) << "Source File:"   << __FILE__ << "\n"
              << std::setw(22) << "Compiled At:"   << __DATE__ << " " << __TIME__ << "\n"
              << std::setw(22) << "Compiler:"      << get_compiler_info() << " (C++" << (__cplusplus / 100 % 100) << ")\n"
              << std::setw(22) << "Build Flags:"   << get_build_flags() << "\n"
              << std::setw(22) << "Pagmo Version:" << PAGMO_VERSION_MAJOR << "." << PAGMO_VERSION_MINOR << "." << PAGMO_VERSION_PATCH << "\n\n";

    // --- 2. Define Problem & State Intent ---
    const unsigned int dim = 10;
    const unsigned int n_islands = 4;
    const unsigned int pop_size = 20;
    const unsigned int gens_per_step = 500;
    const unsigned int evolve_steps = 5;
    const double goal_fitness = 0.0;

    std::cout << "================================================================================\n";
    std::cout << "OPTIMIZATION INTENT & EXPECTED OUTCOME\n";
    std::cout << "================================================================================\n";
    std::cout << "Intent:\n"
              << "  Minimize the " << dim << "-dimensional Rosenbrock banana function using an\n"
              << "  asynchronous island model (" << n_islands << " islands x " << pop_size << " individuals)\n"
              << "  running Differential Evolution (DE) for " << (gens_per_step * evolve_steps) << " total generations per island.\n\n";
    std::cout << "Expected Outcome:\n"
              << "  - Global optimum decision vector: x* = [1.0, 1.0, ..., 1.0]\n"
              << "  - Global minimum objective value: f(x*) = 0.0\n"
              << "  - Success criterion: Champion fitness < 1.0e-05 and ||x - x*||_2 < 1.0e-02 on all islands.\n\n";

    // --- 3. Execute Parallel Archipelago Evolution ---
    pagmo::problem prob{pagmo::rosenbrock{dim}};
    pagmo::algorithm algo{pagmo::de{gens_per_step}};
    pagmo::archipelago archi{n_islands, algo, prob, pop_size};

    archi.evolve(evolve_steps);
    archi.wait_check();

    // --- 4. Quantify Results Against Goal ---
    std::cout << "================================================================================\n";
    std::cout << "RESULTS SUMMARY (MEASURED VS. GOAL)\n";
    std::cout << "================================================================================\n";
    std::cout << std::left
              << std::setw(9)  << "Island"
              << std::setw(15) << "Measured_f"
              << std::setw(10) << "Goal_f"
              << std::setw(15) << "Diff (f-Goal)"
              << std::setw(15) << "||x - x*||_2"
              << std::setw(10) << "Fevals"
              << "Status" << "\n";
    std::cout << std::string(80, '-') << "\n";

    bool all_passed = true;
    for (std::size_t i = 0; i < archi.size(); ++i) {
        const auto pop = archi[i].get_population();
        const double measured_f = pop.champion_f()[0];
        const double diff_f = measured_f - goal_fitness;
        const auto x_champ = pop.champion_x();
        const auto fevals = pop.get_problem().get_fevals();

        double sq_err = 0.0;
        for (double xi : x_champ) {
            const double dx = xi - 1.0;
            sq_err += dx * dx;
        }
        const double x_dist = std::sqrt(sq_err);
        const bool passed = (measured_f < 1.0e-5) && (x_dist < 1.0e-2);
        all_passed = all_passed && passed;

        std::cout << std::left << std::setw(9) << i
                  << std::scientific << std::setprecision(4)
                  << std::setw(15) << measured_f
                  << std::defaultfloat << std::setw(10) << goal_fitness
                  << std::scientific << std::showpos << std::setw(15) << diff_f << std::noshowpos
                  << std::setw(15) << x_dist
                  << std::defaultfloat << std::setw(10) << fevals
                  << (passed ? "PASS" : "FAIL") << "\n";
    }

    std::cout << std::string(80, '-') << "\n";
    std::cout << "Overall Verification: " << (all_passed ? "SUCCESS" : "FAILURE") << "\n";

    return all_passed ? 0 : 1;
}
