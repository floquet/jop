import numpy as np
import matplotlib.pyplot as plt

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

# Generate theta and phi grids
theta = np.linspace(0, np.pi, 100)
phi = np.linspace(0, 2 * np.pi, 100)
theta_grid, phi_grid = np.meshgrid(theta, phi)

# Compute f(theta, phi)
f_theta_phi = (
    a[0] * Y_10(theta_grid, phi_grid) +
    a[1] * Y_11(theta_grid, phi_grid) +
    a[3] * Y_1m1(theta_grid, phi_grid)
)

# Separate real part (magnitude of the sphere)
f_real = np.real(f_theta_phi)

# Assume the input mesh is a perfect sphere of radius 1
input_radius = 1
computed_radius = f_real

# Calculate the difference
difference = computed_radius - input_radius

# Convert to Cartesian coordinates for plotting
x = np.sin(theta_grid) * np.cos(phi_grid)
y = np.sin(theta_grid) * np.sin(phi_grid)
z = np.cos(theta_grid)

# Plot with difference as coloring guide
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(
    x, y, z, facecolors=plt.cm.viridis(difference),
    rstride=1, cstride=1, antialiased=True
)
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Difference')
ax.set_title('Sphere with Difference Coloring')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
