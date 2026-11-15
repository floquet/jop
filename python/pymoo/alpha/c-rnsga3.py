# https://www.pymoo.org/algorithms/moo/rnsga3.html
# R-NSGA-III

import numpy as np
import pymoo

from pymoo.algorithms.moo.rnsga3 import RNSGA3
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

# provenance
import getpass
import os
import platform
import sys
from datetime import datetime
from pathlib import Path

problem_name = "zdt1"
problem = get_problem(problem_name)
pf = problem.pareto_front()

ref_points = np.array([[0.3, 0.4], [0.8, 0.5]])
pop_per_ref_point = 50
mu = 0.1
n_generations = 300
seed = 1

algorithm = RNSGA3(
    ref_points=ref_points,
    pop_per_ref_point=pop_per_ref_point,
    mu=mu,
)

print(f"\npymoo {pymoo.__version__} | R-NSGA-III | {problem_name.upper()}")
print(f"  Decision space   {problem.n_var} continuous variables, each in [0, 1]")
print(f"  Minimization     {problem.n_obj} objectives, f1 and f2")
print("                   f1 = x1")
print("                   f2 = g - sqrt(g * f1)")
print(f"                   g = 1 + 9 * mean(x2, ..., x{problem.n_var})")
print("  Exact front      f2 = 1 - sqrt(f1)")
print("  Reference points (f1, f2)")
for index, (f1, f2) in enumerate(ref_points, start=1):
    print(f"    {index}. ({f1:g}, {f2:g})")
print(f"  Reference fans   {pop_per_ref_point} directions per point, mu = {mu:g}")
print(f"  Run settings     {n_generations} generations, seed = {seed}", flush=True)

res = minimize(
    problem,
    algorithm=algorithm,
    termination=("n_gen", n_generations),
    pf=pf,
    seed=seed,
    verbose=False,
)

print(f"  Run complete     {res.algorithm.evaluator.n_eval:,} evaluations")
print(f"  Solutions        {len(res.F)} objective pairs returned")

reference_directions = res.algorithm.survival.ref_dirs

plot = Scatter(
    title="ZDT1 with R-NSGA-III",
    labels=[r"$f_1$", r"$f_2$"],
    legend=True,
    tight_layout=True,
)

plot.add(
    pf, plot_type="line", color="black", linewidth=1.2,
    label=r"Exact front  $f_2 = 1 - \sqrt{f_1}$", zorder=2,
)
plot.add(
    res.F, marker="o", s=24, facecolors="none",
    edgecolors="#24557a", linewidths=0.8,
    label="Computed solutions", zorder=3,
)
plot.add(
    ref_points, marker="x", s=48, color="black", linewidths=1.2,
    label="Reference points", zorder=4,
)
ideal = res.algorithm.survival.ideal_point

# The final n_obj entries are the axis directions.
fans = np.split(reference_directions[:-problem.n_obj], len(ref_points))

for fan_number, fan in enumerate(fans):
    indices = np.linspace(0, len(fan) - 1, 7, dtype=int)
    for ray_number, endpoint in enumerate(fan[indices]):
        label = "Sampled reference rays" if fan_number == ray_number == 0 else "_nolegend_"
        plot.add(
            np.vstack([ideal, endpoint]),
            plot_type="line", color="0.65", linewidth=0.7,
            label=label, zorder=1,
        )

plot.add(
    ideal[None, :], marker="s", s=20, color="0.35",
    label="Estimated ideal point", zorder=4,
)

plot.save("plot-rnsga3.png")

# provenance

script = Path(__file__).resolve()
timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

print("\n=== BASIC PROVENANCE ===")
print(f"Timestamp         : {timestamp}")
print(f"User              : {getpass.getuser()}")
print(f"Program           : {script.name}")
print(f"Script path       : {script}")
print(f"Working directory : {Path.cwd()}")
print(f"Plot file         : {Path('plot-rnsga3.png').resolve()}")

print("\n=== SYSTEM ===")
print(f"Hostname          : {platform.node()}")
print(f"Architecture      : {platform.machine()}")
print(f"OS                : {platform.system()} {platform.release()}")

print("\n=== PYTHON ===")
print(f"Version           : {platform.python_version()}")
print(f"Implementation    : {platform.python_implementation()}")
print(f"Executable        : {sys.executable}")
print(f"pymoo             : {pymoo.__version__}")
print(f"pymoo location    : {pymoo.__file__}")
print(f"Spack environment : {os.environ.get('SPACK_ENV') or '(none active)'}")