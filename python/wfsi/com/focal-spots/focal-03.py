"""
plot_spt0.py — Classic wireframe plot of spt[0] with opaque black mesh

Mimics classic lenslet PSF mesh plots (e.g., black-on-white wireframes with labeled axes).
No transparency or shading. Output image saved and plot closed automatically.

Author: ChatGPT-4o for Daniel M. Topa
Date: 2025-06-16
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- Physical parameters (microns) ---
f = 28000.0
λ = 0.325
d = 280.0
theta = λ / 300

# --- Plot configuration ---
η = 1
ε = 1e-3
res = 75
out_path = Path("spt0_wireframe.png")

# --- Domain: match range from -100 to 100 in plot
u = np.linspace(-140, 140, res)  # slightly wider to capture edges cleanly
v = np.linspace(-140, 140, res)
U, V = np.meshgrid(u, v)


# --- spt[0] definition ---
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

# --- Create classic opaque mesh plot ---
fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(111, projection="3d")

# Thin, opaque mesh lines (color='k' = black, linewidth = 0.3)
ax.plot_wireframe(U, V, Z, rstride=2, cstride=2, color="k", linewidth=0.3)

# --- Classic axes labeling and range ---
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_zlim(0, 70)

ax.set_xticks([-100, 0, 100])
ax.set_yticks([-100, 0, 100])
ax.set_zticks([0, 20, 40, 60])

ax.set_xlabel("x (μm)")
ax.set_ylabel("y (μm)")
ax.set_zlabel("Amplitude")

# White background, no shadows, opaque lines
ax.xaxis._axinfo["grid"].update(color=(1, 1, 1, 0))
ax.yaxis._axinfo["grid"].update(color=(1, 1, 1, 0))
ax.zaxis._axinfo["grid"].update(color=(1, 1, 1, 0))

fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Tight layout, no GUI
plt.tight_layout()
plt.savefig(out_path, dpi=300)
plt.close(fig)
