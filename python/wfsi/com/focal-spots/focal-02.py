"""
plot_spt0.py

Generates a wireframe mesh plot of spt[0], a lenslet PSF model.

This version implements the following:
- Physical parameters for a Columbus lenslet (f, λ, d, θ)
- Resolved domain grid with optional ε offset
- Plot generated using matplotlib wireframe (mesh-only, no shading)
- Output image saved and figure closed automatically

Author: ChatGPT-4o for Daniel M. Topa
Date: 2025-06-16
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -- Columbus lenslet parameters (microns) --
f = 28000.0  # focal length
λ = 0.325  # wavelength
d = 280.0  # lenslet size
theta = λ / 300  # angular offset

# -- Plotting configuration --
η = 1  # number of lenslets (span)
ε = 1e-3  # small offset to avoid origin singularities
res = 75  # resolution
out_path = Path("spt0_wireframe.png")  # image output file

# -- Domain setup --
u = np.linspace(-η * d / 2, η * d / 2 + ε, res)
v = np.linspace(-η * d / 2, η * d / 2 + ε, res)
U, V = np.meshgrid(u, v)


# -- spt[0] definition --
def spt0(U, V):
    num = (
        f**2
        * λ**2
        * np.sin((d * np.pi * U) / (f * λ)) ** 2
        * np.sin((d * np.pi * V) / (f * λ)) ** 2
    )
    denom = np.pi**4 * U**2 * V**2
    return np.where(denom == 0, 0, num / denom)


Z = spt0(U, V)

# -- Plotting (wireframe only) --
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

ax.plot_wireframe(U, V, Z, rstride=2, cstride=2, color="black")
ax.set_title("spt[0] — Lenslet PSF")
ax.set_axis_off()

# -- Save and close --
plt.tight_layout()
plt.savefig(out_path, dpi=300)
plt.close(fig)
