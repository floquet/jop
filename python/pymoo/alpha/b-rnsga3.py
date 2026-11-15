# https://www.pymoo.org/algorithms/moo/rnsga3.html
# R-NSGA-III

import numpy as np

from pymoo.algorithms.moo.rnsga3 import RNSGA3
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

problem = get_problem("zdt1")
pf = problem.pareto_front()

# Define reference points
ref_points = np.array([[0.3, 0.4], [0.8, 0.5]])

# Get Algorithm
algorithm = RNSGA3(
    ref_points=ref_points,
    pop_per_ref_point=50,
    mu=0.1)

res = minimize(problem,
               algorithm=algorithm,
               termination=('n_gen', 300),
               pf=pf,
               seed=1,
               verbose=False)

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
