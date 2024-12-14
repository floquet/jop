import os
import sys
import time
import math
import numpy as np
import pwd
import platform
import datetime
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd

# Constants
BASE_DIR = os.path.join( os.path.expanduser( "~" ), "GitHub", "jop", "python", "hii", "spherical-harmonics" )
OBJ_FILE = os.path.join( BASE_DIR, "data", "sphere-d050-01.obj" )
SYMLINK = os.path.join( os.path.expanduser( "~" ), "GitHub" )

# Verify symlink
if not os.path.islink( SYMLINK ):
    raise ValueError( f"Expected symlink at {SYMLINK}, but it was not found." )

def read_obj_file( obj_file ):
    """Step 1: Reading the OBJ file and extracting vertices."""
    print( f"Step 1: Reading the OBJ file: {obj_file}" )
    vertices = []
    with open( obj_file, 'r' ) as file:
        for line in file:
            if line.startswith( 'v ' ):
                parts = line.split()
                vertex = [ float( parts[1] ), float( parts[2] ), float( parts[3] ) ]
                vertices.append( vertex )
    print( f"Extracted {len( vertices )} vertices from the OBJ file." )
    return np.array( vertices )

def spherical_coordinates(vertices):
    """Convert vertices to spherical coordinates and generate a mesh grid."""
    print("Step 2: Converting vertices to spherical coordinates.")
    x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
    r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)

    # Create a mesh grid
    theta_grid, phi_grid = np.meshgrid(theta, phi)

    return r, theta_grid, phi_grid

def compute_spherical_harmonics( theta, phi, order = 1 ):
    """Compute spherical harmonic amplitudes."""
    print( f"Step 3: Computing spherical harmonic amplitudes up to order {order}." )
    coefficients = []
    for l in range( order + 1 ):
        for m in range( -l, l + 1 ):
            Y_lm = ( np.sqrt( ( 2 * l + 1 ) / ( 4 * np.pi ) * math.factorial( l - abs( m ) ) / math.factorial( l + abs( m ) ) ) *
                     np.exp( 1j * m * phi ) *
                     np.polynomial.legendre.legval( np.cos( theta ), [0] * abs( m ) + [1] ) )
            coefficients.append( Y_lm )
    print( f"Computed {len( coefficients )} coefficients." )
    return np.array( coefficients )

def plot_spherical_surface(theta, phi, r, arg, original_vertices):
    """Plot the spherical harmonic approximation as a surface."""
    print("Step 4: Plotting spherical harmonic approximation as a surface.")

    # Convert spherical to Cartesian for surface plotting
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    # Ensure arguments are 2D
    if len(x.shape) != 2 or len(y.shape) != 2 or len(z.shape) != 2:
        raise ValueError("x, y, and z must be 2-dimensional arrays.")

    # Plot the surface
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(
        x, y, z, facecolors=plt.cm.viridis(arg), rstride=1, cstride=1, antialiased=True
    )

    # Overlay original vertices as points
    ax.scatter(
        original_vertices[:, 0],
        original_vertices[:, 1],
        original_vertices[:, 2],
        color="blue",
        s=1,
        label="Original",
    )

    # Enhance the plot
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
    ax.set_title("Sphere Approximation with Argument Coloring")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()

    plt.show()


def compute_differences( vertices, approximations ):
    """Compute and display differences between original and approximated vertices."""
    differences = np.linalg.norm( vertices - approximations, axis = 1 )
    data = np.hstack( ( vertices, approximations, differences[:, None] ) )
    df = pd.DataFrame( data, columns = [ "X_orig", "Y_orig", "Z_orig", "X_approx", "Y_approx", "Z_approx", "Difference" ] )
    print( df.head() )
    return df

def pr_provenance():
    """Print system provenance."""
    print( "\nExecution Provenance" )
    print( "=" * 40 )
    print( "\n", datetime.datetime.now() )
    print( "source:  %s/%s" % ( os.getcwd(), os.path.basename( __file__ ) ) )
    print( "user id:", pwd.getpwuid( os.getuid() ).pw_name )
    print( "platform info:" )
    print( "    platform: ", platform.platform() )
    print( "    uname:    ", platform.uname() )
    print( "version info:" )
    print( "    python:   %s" % sys.version )
    print( "    numpy:   ", np.__version__ )
    cpu_time = time.process_time()
    print( f"    CPU time used: {cpu_time:.2f} seconds" )
    print( "=" * 40 )

# Main execution
if __name__ == "__main__":
    vertices = read_obj_file( OBJ_FILE )
    r, theta, phi = spherical_coordinates( vertices )
    amplitudes = compute_spherical_harmonics( theta, phi, order = 1 )
    
    # Create normalized radius and compute argument
    r_normalized = r / np.max( r )
    arg = np.angle( amplitudes[0] )  # Use the first term for simplicity
    
    # Plot spherical harmonic surface
    plot_spherical_surface( theta, phi, r_normalized, arg, vertices )
    
    # Compute differences for reporting
    differences_df = compute_differences( vertices, vertices )  # Approximation currently same as vertices
    
    pr_provenance()
