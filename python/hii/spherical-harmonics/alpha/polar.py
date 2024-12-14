import numpy as np
import matplotlib.pyplot as plt

# Generate theta and phi
theta = np.linspace(0, np.pi, 100)  # Polar angle
phi = np.linspace(0, 2 * np.pi, 100)  # Azimuthal angle
theta_grid, phi_grid = np.meshgrid(theta, phi)

# Constant radius
r = np.ones_like(theta_grid)

# Plot the sphere in polar coordinates
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(8, 6))
contour = ax.contourf(phi_grid, np.pi - theta_grid, r, levels=50, cmap='viridis')

# Enhance the plot
ax.set_title("Sphere in Polar Coordinates ($f(\\theta, \\phi) = 1$)")
plt.colorbar(contour, label='Radius (r)')
plt.show()
