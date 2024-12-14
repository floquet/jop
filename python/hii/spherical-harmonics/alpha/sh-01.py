import os
import sys
import time
import math
import numpy as np
import pwd
import platform
import datetime

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
                vertex = [float( parts[1] ), float( parts[2] ), float( parts[3] )]
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

def compute_spherical_harmonics( theta, phi, order=1 ):
    """Compute spherical harmonic amplitudes."""
    print( f"Step 3: Computing spherical harmonic amplitudes up to order {order}." )
    coefficients = []
    for l in range( order + 1 ):
        for m in range( -l, l + 1 ):
            Y_lm = np.sqrt( (2 * l + 1) / (4 * np.pi) * math.factorial( l - abs( m ) ) / math.factorial( l + abs( m ) ) ) * \
                   np.exp( 1j * m * phi ) * np.polynomial.legendre.legval( np.cos( theta ), [0] * abs( m ) + [1] )
            coefficients.append( Y_lm )
    print( f"Computed {len( coefficients )} coefficients." )
    return np.array( coefficients )

def plot_approximation( vertices, theta, phi, amplitudes ):
    """Plot the spherical harmonic approximation in 3D."""
    print( "Step 4: Plotting spherical harmonic approximation in 3D." )
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    approximation = np.zeros_like( theta, dtype=np.complex128 )
    for amp, ( th, ph ) in zip( amplitudes, zip( theta, phi ) ):
        approximation += amp * np.exp( 1j * ph ) * np.polynomial.legendre.legval( np.cos( th ), [1] )

    x_approx = np.real( approximation ) * np.sin( theta ) * np.cos( phi )
    y_approx = np.real( approximation ) * np.sin( theta ) * np.sin( phi )
    z_approx = np.real( approximation ) * np.cos( theta )

    fig = plt.figure()
    ax = fig.add_subplot( 111, projection='3d' )
    ax.scatter( vertices[:, 0], vertices[:, 1], vertices[:, 2], color='blue', label='Original' )
    ax.scatter( x_approx, y_approx, z_approx, color='red', label='Approximation' )
    ax.legend()
    plt.show()

def pr_provenance():
    """Print system provenance."""
    print( "\nExecution Provenance" )
    print( "=" * 40 )
    print( "\n", datetime.datetime.now() )
    print( "source:  %s/%s" % ( os.getcwd(), os.path.basename( __file__ ) ) )
    print( "user id:", pwd.getpwuid( os.getuid() ).pw_name )
    print( "platform info:" )
    print( "    platform: ", platform.platform( ) )
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
    amplitudes = compute_spherical_harmonics( theta, phi, order=1 )
    plot_approximation( vertices, theta, phi, amplitudes )
    pr_provenance()
