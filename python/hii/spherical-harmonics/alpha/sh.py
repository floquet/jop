import os
import pwd
import platform
import sys
import datetime
import numpy as np
from scipy.linalg import lstsq
from scipy.special import sph_harm
import matplotlib.pyplot as plt

# Define the directory structure as variables
BASE_DIR = "/Users/dantopa/repos-xiuhcoatal/github/jop/python/hii"
GEO_DIR = os.path.join( BASE_DIR, "geo" )
GEO_UTILS_DIR = os.path.join( BASE_DIR, "geo-utils" )
SPHERICAL_HARMONICS_DIR = os.path.join( BASE_DIR, "spherical-harmonics" )
SPH_DATA_DIR = os.path.join( SPHERICAL_HARMONICS_DIR, "data" )

SPHERE_D050_01 = os.path.join( SPH_DATA_DIR, "sphere-d050-01.obj" )

# Provenance function
def pr_provenance():
    """
    Print the provenance information of the script including execution
    details, user information, platform details, and package versions.
    """
    print( "\nExecution Provenance" )
    print( "=" * 40 )
    print( "Execution Time:", datetime.datetime.now() )
    print( "Source Path:   {}/{}".format( os.getcwd(), os.path.basename( __file__ ) ) )
    print( "User ID:       {}".format( pwd.getpwuid( os.getuid() ).pw_name ) )
    print( "\nPlatform Information:" )
    print( "    Platform:  {}".format( platform.platform() ) )
    print( "    System:    {}".format( platform.uname().system ) )
    print( "    Node:      {}".format( platform.uname().node ) )
    print( "    Release:   {}".format( platform.uname().release ) )
    print( "    Version:   {}".format( platform.uname().version ) )
    print( "    Machine:   {}".format( platform.uname().machine ) )
    print( "    Processor: {}".format( platform.uname().processor ) )
    print( "\nVersion Information:" )
    print( "    Python:    {}".format( sys.version.splitlines()[0] ) )
    print( "    NumPy:     {}".format( np.__version__ ) )
    print( "    Platform:  {}".format( platform.__version__ ) )
    print( "=" * 40 )
    return

# Step 1: Reading the OBJ File
def read_obj_vertices( obj_file ):
    """
    Reads the vertices from an OBJ file and returns them as a list of 3D points.
    """
    print( f"Step 1: Reading *.obj file: {obj_file}" )
    vertices = []
    with open( obj_file, "r" ) as file:
        for line in file:
            if line.startswith( "v " ):
                parts = line.split()
                vertices.append( [ float( parts[1] ), float( parts[2] ), float( parts[3] ) ] )
    return np.array( vertices )

# Step 2: Convert Cartesian to Spherical Coordinates
def cartesian_to_spherical( vertices ):
    """
    Converts a list of 3D Cartesian points to spherical coordinates.
    """
    print( "Step 2: Converting Cartesian coordinates to spherical coordinates" )
    x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
    r = np.sqrt( x ** 2 + y ** 2 + z ** 2 )
    theta = np.arccos( z / r )  # Inclination
    phi = np.arctan2( y, x )    # Azimuth
    return theta, phi

# Step 3: Compute Spherical Harmonic Amplitudes
def compute_spherical_harmonics( theta, phi, max_order = 1 ):
    """
    Computes the amplitudes of spherical harmonics up to a given order.
    """
    print( f"Step 3: Computing spherical harmonics up to order {max_order}" )
    n_points = len( theta )
    n_harmonics = ( max_order + 1 ) ** 2
    b_matrix = np.zeros( ( n_points, n_harmonics ), dtype = complex )
    idx = 0
    for l in range( max_order + 1 ):
        for m in range( -l, l + 1 ):
            b_matrix[:, idx] = sph_harm( m, l, phi, theta )
            idx += 1
    return b_matrix

def least_squares_fit( b_matrix, f_values ):
    """
    Solves the least-squares problem to find the spherical harmonic amplitudes.
    """
    print( "Step 4: Solving least-squares system for amplitudes" )
    amplitudes, residuals, _, _ = lstsq( b_matrix, f_values )
    print( "Amplitudes:" )
    for i, amp in enumerate( amplitudes ):
        print( f"    a[{i}] = {amp}" )
    print( f"Residual Error: {residuals}" )
    return amplitudes, residuals

# Step 5: Plot the Approximation
def plot_spherical_harmonics( amplitudes, theta, phi ):
    """
    Plots the spherical harmonic approximation in 3D.
    """
    print( "Step 5: Plotting spherical harmonic approximation in 3D" )
    n_points = len( theta )
    f_approx = np.zeros( n_points, dtype = complex )
    idx = 0
    for l in range( 2 ):  # Up to order 1
        for m in range( -l, l + 1 ):
            f_approx += amplitudes[idx] * sph_harm( m, l, phi, theta )
            idx += 1

    x = np.sin( theta ) * np.cos( phi ) * np.real( f_approx )
    y = np.sin( theta ) * np.sin( phi ) * np.real( f_approx )
    z = np.cos( theta ) * np.real( f_approx )

    fig = plt.figure()
    ax = fig.add_subplot( 111, projection = "3d" )
    ax.scatter( x, y, z, c = np.abs( f_approx ), cmap = "viridis" )
    ax.set_title( "Spherical Harmonic Approximation" )
    plt.show()

# Main execution
if __name__ == "__main__":
    # Provenance
    pr_provenance()

    # Step 1: Read OBJ file
    vertices = read_obj_vertices( SPHERE_D050_01 )

    # Step 2: Convert to spherical coordinates
    theta, phi = cartesian_to_spherical( vertices )

    # Step 3: Compute spherical harmonics and amplitudes
    b_matrix = compute_spherical_harmonics( theta, phi, max_order = 1 )
    f_values = np.ones( len( theta ) )  # Example function values (all ones)
    amplitudes, residuals = least_squares_fit( b_matrix, f_values )

    # Step 4: Plot the approximation
    plot_spherical_harmonics( amplitudes, theta, phi )
