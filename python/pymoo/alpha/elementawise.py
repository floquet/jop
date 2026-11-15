
# ChatGPT
# Sat Nov 14 12:30:17 MST 2026
# https://pymoo.org/

import numpy as np
from pymoo.core.problem import ElementwiseProblem

class AdvertisingProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=2,
            xl=np.array([0, 0]),
            xu=np.array([28, 28]),
            vtype=int
        )

    def _evaluate(self, x, out, *args, **kwargs):
        j, k = x

        out["F"] = [j, k]

        out["G"] = [
            8 - j - k,
            28 - j - 5*k
        ]
