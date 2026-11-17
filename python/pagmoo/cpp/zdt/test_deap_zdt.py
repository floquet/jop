#!/usr/bin/env python3
"""Verify DEAP NSGA-II integration with C++ pagmo2 ZDT1 benchmark."""

import random
import sys

try:
    from deap import algorithms, base, creator, tools
except ImportError as exc:
    sys.exit(f"ERROR: DEAP not installed ({exc}). Install via: sudo apt-get install -y python3-deap")

import pagmo_benchmarks


def main() -> int:
    random.seed(42)

    # 1. Connect to pagmo::zdt(1, 30) -> ZDT1 with 30 decision variables, 2 objectives
    bench = pagmo_benchmarks.PagmoBenchmark(suite="zdt", prob_id=1, dim=30)
    lb, ub = bench.get_bounds()
    n_dim = bench.get_nx()
    n_obj = bench.get_nobj()

    print(f"Benchmark:  {bench.get_name()}")
    print(f"Dimensions: nx={n_dim}, nobj={n_obj}")

    # 2. Configure DEAP minimization types
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,) * n_obj)
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.uniform, 0.0, 1.0)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=n_dim)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # 3. Register C++ pagmo::zdt::fitness() directly as DEAP's evaluate callable
    toolbox.register("evaluate", bench.evaluate)
    toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=lb, up=ub, eta=20.0)
    toolbox.register("mutate", tools.mutPolynomialBounded, low=lb, up=ub, eta=20.0, indpb=1.0 / n_dim)
    toolbox.register("select", tools.selNSGA2)

    # 4. Run NSGA-II for 100 generations
    pop_size = 100
    ngen = 100
    pop = toolbox.population(n=pop_size)
    algorithms.eaMuPlusLambda(
        pop, toolbox, mu=pop_size, lambda_=pop_size, cxpb=0.9, mutpb=0.1, ngen=ngen, verbose=False
    )

    front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]
    f_sorted = sorted(ind.fitness.values for ind in front)

    print(f"Front size: {len(front)} / {pop_size}")
    print(f"Anchor F_min_f1: ({f_sorted[0][0]:.6f}, {f_sorted[0][1]:.6f})")
    print(f"Anchor F_max_f1: ({f_sorted[-1][0]:.6f}, {f_sorted[-1][1]:.6f})")

    # Verify convergence near the analytical ZDT1 Pareto front: f2 = 1 - sqrt(f1), g -> 1
    assert len(front) >= 50, f"FAILED: Pareto front too small ({len(front)})"
    assert f_sorted[0][1] < 1.15, f"FAILED: Poor ZDT1 convergence (f2={f_sorted[0][1]})"

    print("PASS: DEAP <-> pagmo2 ZDT1 pybind11 bridge verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
