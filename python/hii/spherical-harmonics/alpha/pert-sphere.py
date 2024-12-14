import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define spherical harmonics
def Y_1m1(theta, phi):
    return np.sqrt(3 / (8 * np.pi)) * np.sin(theta) * np.exp(-1j * phi)

def Y_10(theta, phi):
    return np.sqrt(3 / (4 * np.pi)) * np.cos(theta)

def Y_11(theta, phi):
    return -np.sqrt(3 / (8 * np.pi)) * np.sin(theta) * np.exp(1j * phi)

# Perturbation magnitude
epsilon = 1e-6

# Amplitudes for first-order harmonics (arbitrary small perturbation values)
a_1m1 = epsilon
a_10 = epsilon
a_11 = epsilon

# Generate spherical coordinates
theta = np.linspace(0, np.pi, 100)  # Polar angle
phi = np.linspace(0, 2 * np.pi, 100)  # Azimuthal angle
theta_grid, phi_grid = np.meshgrid(theta, phi)

# Compute f(theta, phi) with perturbations
f_theta_phi = 1 + a_1m1 * Y_1m1(theta_grid, phi_grid) + \
                  a_10 * Y_10(theta_grid, phi_grid) + \
                  a_11 * Y_11(theta_grid, phi_grid)

# Resolve the real part (ignore imaginary for visualization)
f_theta_phi_real = np.real(f_theta_phi)

# Map to Cartesian coordinates
x = f_theta_phi_real * np.sin(theta_grid) * np.cos(phi_grid)
y = f_theta_phi_real * np.sin(theta_grid) * np.sin(phi_grid)
z = f_theta_phi_real * np.cos(theta_grid)

# Plot the perturbed sphere
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x, y, z, cmap='coolwarm', alpha=0.8)

# Enhance the visualization
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
ax.set_title("Perturbed Sphere with First-Order Terms")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.show()
