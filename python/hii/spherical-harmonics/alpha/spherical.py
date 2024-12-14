import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generate theta and phi for spherical coordinates
theta = np.linspace(0, np.pi, 100)  # Polar angle
phi = np.linspace(0, 2 * np.pi, 100)  # Azimuthal angle
theta_grid, phi_grid = np.meshgrid(theta, phi)

# Radius of the sphere
r = 1

# Convert to Cartesian coordinates for plotting
x = r * np.sin(theta_grid) * np.cos(phi_grid)
y = r * np.sin(theta_grid) * np.sin(phi_grid)
z = r * np.cos(theta_grid)

# Plot the sphere as a surface
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, cmap='viridis', alpha=0.8)

# Enhance the visualization
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
ax.set_title("True 3D Sphere")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.show()
