import os
import sys
import time
import math
import numpy as np
import pwd
import platform
import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Constants
BASE_DIR = os.path.join(os.path.expanduser("~"), "GitHub", "jop", "python", "hii", "spherical-harmonics")
OBJ_FILE = os.path.join(BASE_DIR, "data", "sphere-d050-01.obj")
SYMLINK = os.path.join(os.path.expanduser("~"), "GitHub")

# Verify symlink
if not os.path.islink(SYMLINK):
    raise ValueError(f"Expected symlink at {SYMLINK}, but it was not found.")

def read_obj_file(obj_file):
    """Step 1: Reading the OBJ file and extracting vertices."""
    print(f"Step 1: Reading the OBJ file: {obj_file}")
    vertices = []
    with open(obj_file, "r") as file:
        for line in file:
            if line.startswith("v "):
                parts = line.split()
                vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(vertex)
    print(f"Extracted {len(vertices)} vertices from the OBJ file.")
    return np.array(vertices)

def spherical_coordinates(vertices):
    """Convert vertices to spherical coordinates and generate a mesh grid."""
    print("Step 2: Converting vertices to spherical coordinates.")
    x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)
    return r, theta, phi

def compute_spherical_harmonics(theta, phi, order=1):
    """Compute spherical harmonic amplitudes."""
    print(f"Step 3: Computing spherical harmonic amplitudes up to order {order}.")
    coefficients = []
    for l in range(order + 1):
        for m in range(-l, l + 1):
            Y_lm = (
                np.sqrt((2 * l + 1) / (4 * np.pi) * math.factorial(l - abs(m)) / math.factorial(l + abs(m)))
                * np.exp(1j * m * phi)
                * np.polynomial.legendre.legval(np.cos(theta), [0] * abs(m) + [1])
            )
            coefficients.append(Y_lm)
    print(f"Computed amplitudes:")
    for i, coef in enumerate(coefficients):
        print(f"a[{i}] = {np.mean(coef)}")  # Show mean amplitude for each component
    return np.array(coefficients)

def plot_spherical_surface(theta, phi, computed_radius, difference, original_vertices, label=""):
    """Plot the spherical harmonic approximation as a surface."""
    print(f"Step 4: Plotting spherical harmonic approximation with {label}.")
    x = computed_radius * np.sin(theta) * np.cos(phi)
    y = computed_radius * np.sin(theta) * np.sin(phi)
    z = computed_radius * np.cos(theta)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(
        x, y, z, facecolors=plt.cm.viridis(difference), rstride=1, cstride=1, antialiased=True
    )
    ax.scatter(original_vertices[:, 0], original_vertices[:, 1], original_vertices[:, 2], color="blue", s=1, label="Original")
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label=label)
    ax.set_title(f"Sphere with {label} Coloring")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()

def compute_differences(vertices, computed_radius, theta, phi):
    """Compare input points and computed values at theta, phi."""
    print("Step 5: Computing differences between input and computed values.")
    x_input, y_input, z_input = vertices[:, 0], vertices[:, 1], vertices[:, 2]
    x_computed = computed_radius * np.sin(theta) * np.cos(phi)
    y_computed = computed_radius * np.sin(theta) * np.sin(phi)
    z_computed = computed_radius * np.cos(theta)
    differences = np.sqrt((x_input - x_computed)**2 + (y_input - y_computed)**2 + (z_input - z_computed)**2)
    data = np.column_stack((x_input, y_input, z_input, x_computed, y_computed, z_computed, differences))
    df = pd.DataFrame(data, columns=["X_orig", "Y_orig", "Z_orig", "X_comp", "Y_comp", "Z_comp", "Difference"])
    print(df.head())
    return df

def pr_provenance():
    """Print system provenance."""
    print("\nExecution Provenance")
    print("=" * 40)
    print("\n", datetime.datetime.now())
    print("source:  %s/%s" % (os.getcwd(), os.path.basename(__file__)))
    print("user id:", pwd.getpwuid(os.getuid()).pw_name)
    print("platform info:")
    print("    platform: ", platform.platform())
    print("    uname:    ", platform.uname())
    print("version info:")
    print("    python:   %s" % sys.version)
    print("    numpy:   ", np.__version__)
    print("    pandas:  ", pd.__version__)
    print("    matplotlib: ", plt.matplotlib.__version__)
    print("=" * 40)

# Main execution
if __name__ == "__main__":
    # Step 1: Read the OBJ file to extract vertices
    vertices = read_obj_file(OBJ_FILE)

    # Step 2: Convert vertices to spherical coordinates
    r, theta, phi = spherical_coordinates(vertices)

    # Step 3: Compute the spherical harmonic amplitudes
    amplitudes = compute_spherical_harmonics(theta, phi, order=1)

    # Compute the spherical harmonic approximation for the surface
    computed_radius = np.abs(amplitudes[0]) * np.ones_like(theta)  # Create a 2D array matching theta, phi
    r_grid = r[:, None] * np.ones_like(phi)  # Reshape r to match the grid shape
    difference = computed_radius - r_grid  # Compute the pointwise difference

    # Step 4: Plot Real and Imaginary Parts of f(theta, phi)
    plot_spherical_surface(
        theta, phi, computed_radius, np.real(computed_radius), vertices, label="Re(f)"
    )
    plot_spherical_surface(
        theta, phi, computed_radius, np.imag(computed_radius), vertices, label="Im(f)"
    )

    # Step 5: Plot the difference as a coloring guide
    plot_spherical_surface(
        theta, phi, computed_radius, difference, vertices, label="Difference"
    )

    # Step 6: Compute and display differences for input and computed values
    differences_df = compute_differences(vertices, computed_radius, theta, phi)

    # Step 7: Print system provenance
    pr_provenance()

