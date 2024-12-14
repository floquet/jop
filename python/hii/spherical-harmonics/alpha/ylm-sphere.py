import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define spherical harmonics for l=0, m=0
def Y_00(theta, phi):
    return np.sqrt(1 / (4 * np.pi))  # Constant over the sphere

# Amplitude for f(theta, phi) = 1
a_00 = np.sqrt(4 * np.pi)  # From decomposition

# Generate spherical coordinates
theta = np.linspace(0, np.pi, 100)  # Polar angle
phi = np.linspace(0, 2 * np.pi, 100)  # Azimuthal angle
theta_grid, phi_grid = np.meshgrid(theta, phi)

# Compute f(theta, phi)
f_theta_phi = a_00 * Y_00(theta_grid, phi_grid)  # Should be constant 1

# Map to Cartesian
x = f_theta_phi * np.sin(theta_grid) * np.cos(phi_grid)
y = f_theta_phi * np.sin(theta_grid) * np.sin(phi_grid)
z = f_theta_phi * np.cos(theta_grid)

# Plot the reconstructed sphere
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, cmap='viridis', alpha=0.8)

# Enhance the visualization
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
ax.set_title("Reconstructed Sphere from Spherical Harmonics")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.show()
p