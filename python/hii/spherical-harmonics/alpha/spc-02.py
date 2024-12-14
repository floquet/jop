import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define spherical harmonics Y_l^m for l=1
def Y_1m1(theta, phi):
    return np.sqrt(3 / (8 * np.pi)) * np.sin(theta) * np.exp(-1j * phi)

def Y_10(theta, phi):
    return np.sqrt(3 / (4 * np.pi)) * np.cos(theta)

def Y_11(theta, phi):
    return -np.sqrt(3 / (8 * np.pi)) * np.sin(theta) * np.exp(1j * phi)

# Amplitudes
a = [
    (3.5449077018110335+0j),  # a[0], m = 0
    (7.691791905180097e-17+2.3672900863491923e-16j),  # a[1], m = 1
    (1.7600708975250343e-16+1.4791141972893971e-31j),  # a[2], m = 2
    (-7.691791905180091e-17+2.36729008634919e-16j)   # a[3], m = -1
]

# Generate spherical coordinates
theta = np.linspace(0, np.pi, 100)  # Polar angle
phi = np.linspace(0, 2 * np.pi, 100)  # Azimuthal angle
theta_grid, phi_grid = np.meshgrid(theta, phi)

# Compute the reconstructed function f(theta, phi)
f_theta_phi = (
    a[0] * Y_10(theta_grid, phi_grid) +
    a[1] * Y_11(theta_grid, phi_grid) +
    a[3] * Y_1m1(theta_grid, phi_grid)  # Note: a[3] is for m=-1
)

# Theoretical radius
r_theoretical = 2 * np.sqrt(np.pi)

# Reconstructed radius (real part of f(theta, phi))
r_reconstructed = np.real(f_theta_phi)

# Compute difference
r_difference = r_theoretical - r_reconstructed

# Plot the reconstructed sphere
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Convert reconstructed radius to Cartesian
x = r_reconstructed * np.sin(theta_grid) * np.cos(phi_grid)
y = r_reconstructed * np.sin(theta_grid) * np.sin(phi_grid)
z = r_reconstructed * np.cos(theta_grid)

surf = ax.plot_surface(x, y, z, cmap='viridis', alpha=0.8)

# Enhance the visualization
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
ax.set_title("Reconstructed Sphere from Amplitudes")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.show()

# Heatmap of differences
plt.figure(figsize=(8, 6))
plt.pcolormesh(phi, theta, r_difference, shading='auto', cmap='coolwarm')
plt.colorbar(label='Radius Difference (Δr)')
plt.title('Difference Between Input and Output Radii')
plt.xlabel('Phi (azimuthal angle)')
plt.ylabel('Theta (polar angle)')
plt.show()

# Print summary of differences
print(f"Maximum Difference: {np.max(np.abs(r_difference)):.6f}")
print(f"Average Difference: {np.mean(np.abs(r_difference)):.6f}")
