import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Set up domain
u = np.linspace(-50, 50, 400)
v = np.linspace(-10, 10, 400)
U, V = np.meshgrid(u, v)

# Avoid division by zero
epsilon = 1e-8
U_safe = np.where(U == 0, epsilon, U)
V_safe = np.where(V == 30.3333, 30.3333 + epsilon, V)

# Define function
Z = (
    850126
    * np.sin(0.0966644 * U_safe) ** 2
    * np.sin(0.0966644 * (-30.3333 + V_safe)) ** 2
) / (U_safe**2 * (-30.3333 + V_safe) ** 2)

# Plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

# Wireframe only (no surface fill)
ax.plot_wireframe(U, V, Z, rstride=10, cstride=10, color="black")

# Optional: turn off axes and box for pure mesh view
ax.set_axis_off()

plt.tight_layout()
plt.show()
