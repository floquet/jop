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

def spherical_coordinates( vertices ):
    """Convert vertices to spherical coordinates."""
    print( "Step 2: Converting vertices to spherical coordinates." )
    x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
    r = np.sqrt( x ** 2 + y ** 2 + z ** 2 )
    theta = np.arccos( z / r )
    phi = np.arctan2( y, x )
    return r, theta, phi

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

def plot_approximation( vertices, r, theta, phi, amplitudes ):
    """Plot the spherical harmonic approximation in 3D."""
    print( "Step 4: Plotting spherical harmonic approximation in 3D." )

    # Approximate the radius
    approx_r = np.real( amplitudes[0] )  # Use only the first term as a simplification
    x_approx = approx_r * np.sin( theta ) * np.cos( phi )
    y_approx = approx_r * np.sin( theta ) * np.sin( phi )
    z_approx = approx_r * np.cos( theta )

    # Plot the original and approximated vertices
    fig = plt.figure()
    ax = fig.add_subplot( 111, projection = '3d' )
    ax.scatter( vertices[:, 0], vertices[:, 1], vertices[:, 2], color = 'blue', label = 'Original' )
    ax.scatter( x_approx, y_approx, z_approx, color = 'red', label = 'Approximation' )
    ax.legend()
    plt.show()

    return np.column_stack( ( x_approx, y_approx, z_approx ) )

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
    approximations = plot_approximation( vertices, r, theta, phi, amplitudes )
    differences_df = compute_differences( vertices, approximations )
    pr_provenance()
