This example asks **“Can R-NSGA-III find Pareto-optimal tradeoffs in two regions I care about?”** ZDT1 makes that easy to check because its exact Pareto front is known.

### What it optimizes

ZDT1 has 30 continuous decision variables and two objectives to minimize. Every candidate `x` maps to a point \((f_1(x),f_2(x))\) in the plot. The exact Pareto front is

\[
f_2 = 1-\sqrt{f_1}, \qquad 0\le f_1\le 1.
\]

That curve is the objective-space counterpart of the frontier in your ads-and-appearances example. Here the tradeoff is continuous. [pymoo.org](https://pymoo.org/problems/multi/zdt.html?utm_source=chatgpt.com)

### How the two points guide the search

`ref_points` gives two preferences in **objective space**. For example, \((0.3,0.4)\) lies almost on the front, since at \(f_1=0.3\) the front has \(f_2\approx0.452\). The second point, \((0.8,0.5)\), sits well above the front, which has \(f_2\approx0.106\) at that \(f_1\).

R-NSGA-III builds a group of reference directions for each preference. `pop_per_ref_point=50` sets the number of directions per group, and `mu=0.1` controls how tightly they are grouped. When a nondominated front has more candidates than available slots, the algorithm uses those directions to decide which candidates survive. The reference points guide **where to concentrate coverage**. The exact front `pf` provides a benchmark for comparison. [pymoo.org](https://pymoo.org/algorithms/moo/rnsga3.html?utm_source=chatgpt.com)

### What the plot shows

| Label | Meaning |
|---|---|
| `pf` | The exact ZDT1 Pareto front, sampled for plotting |
| `F` | The objective pairs `res.F` returned after 300 generations |
| `ref_points` | The two preference points you supplied |
| `ref_dirs` | The final reference direction vectors drawn as dots at their component coordinates |

Read the `F` dots against the `pf` curve. **The gap to the curve shows how closely the run approximated the front. The distribution along the curve shows where the algorithm spent its coverage.** Each row of `res.X` gives the 30 decision variables corresponding to the same row of `res.F`. [pymoo.org](https://pymoo.org/algorithms/moo/rnsga3.html?utm_source=chatgpt.com)
