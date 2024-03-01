#! /opt/local/bin/python
#! /home/dantopa/spacktivity/ubuntu-22.04-dantopa-docker-spack/opt/spack/linux-ubuntu22.04-haswell/gcc-12.2.0/python-3.10.6-ybcookynohghdr6i72gwalqle6hq27z5/bin/python
# Solving Bevington example 6.1 with Python
import datetime             # timestamps
import numpy as np          # array operations
import os                   # opeating system
import platform             # uname
import pwd
import sys                  # python version

# # computation modules
def least_squares( x, y ):
    # least squares solution for intercept of logarithmic transform a0
    a0 = np.average( y ) - np.average( x )
    # error propagation
    residualV = a0 - y + x
    t2 = np.dot( residualV, residualV )
    sigma = np.sqrt( t2 / m / (m - 1) )
    return ( a0, sigma );

# # load modules
def load_radius_time( ):

    # The Formation of a Blast Wave by a Very Intense Explosion II. The Atomic Explosion of 1945
    # Geoffrey Ingram Taylor
    # Table 1, p. 176
    # time: s
    # radius: cm
    t = np.array( [ 0.0001, 0.00024, 0.00038, 0.00052, 0.00066, 0.0008, 0.00094, 0.00108, 0.00122, 0.00136, 0.0015, 0.00165, 0.00179, 0.00193, 0.00326, 0.00353, 0.0038, 0.00407, 0.00434, 0.00461, 0.015, 0.025, 0.034, 0.053, 0.062 ] )
    r = np.array( [ 1110., 1990., 2540., 2880., 3190., 3420., 3630., 3890., 4100., 4280., 4440., 4600., 4690., 4870., 5900., 6110., 6290., 6430., 6560., 6730., 10650., 13000., 14500., 17500., 18500. ] )
    # print ( "observation times t =", np.matrix( t ) )
    m = t.size

    return ( t, r, m );

def load_parameters( ):

    # p. 178
    gamma      = 1.4
    rhoTaylor  = 0.00125
    # U.S. Standard atmosphere for 1500 m elevation
    rhoTrinity = 0.00105807

    rho = rhoTaylor

    # Table 3, p. 180
    I1 = 0.185
    I2 = 0.187

    # Energy partition - kinetic + potential
    # (7) p. 178
    K = 2 * np.pi * I1
    K = K + 4 * np.pi * I2 / gamma / ( gamma - 1 )
    K = 4 * K / 25

    return ( gamma, rho, K );

# # probe modules
def pr_parameters ( gamma, rho, K ):
    print ( gamma, " gamma, adiabtic constant, ideal diatomic gas (pure)" )
    print ( rho, " air density g/cc" ) 
    print ( K, " total energy (pure)" )
    return;

def pr_provenance():
    print( "\n", datetime.datetime.now( ) )
    print( "source:  %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
    print( "user id:", pwd.getpwuid( os.getuid( ) ).pw_name )
    print( "platform info:")
    print( "    platform: ", platform.platform() )
    print( "    uname:    ", platform.uname() )
    #print( "    node:     ", platform.node( ) )
    #print( os.environ )
    print( "version info:")
    print( "    python:   %s" % sys.version )
    print( "    numpy:   ", np.__version__ )
    print( "    platform:", platform.__version__ )
    return;

#  ==   ==   == ==   ==   == ==   ==   == ==   ==   ==  #

if __name__ == "__main__":

# 1. load time, radius measurements
# 2. load parameters
# 3. compute logarithmic transform
# 4. least squares solution

    ( t, r, m ) = load_radius_time( )
    print ( "data points loaded: m = ", m )

    ( gamma, rho, K ) = load_parameters( )
    pr_parameters ( gamma, rho, K )

    # logarithmic transforms of input data
    x =         np.log10( t )
    y = 5 / 2 * np.log10( r )

    # least squares solution for intercept
    ( a0, sigma ) = least_squares( x, y )
    print ( "least squares solution = ", a0, " +/- ", sigma ) 

    # numpy.linalg.LinAlgError: 1-dimensional array given. Array must be two-dimensional
    # A = np.ones( m )
    # ls = np.linalg.lstsq( A, y - x )
    # print ( "least squares np.linalg.lstsq = ", ls ) 

    # shut down with provenance
    pr_provenance( )

# dantopa@Quaxolotl.local:taylor $ python3 fireball-01.py 
# data points loaded: m =  25
# 1.4  gamma, adiabtic constant, ideal diatomic gas (pure)
# 0.00125  air density g/cc
# 0.8573855150597061  total energy (pure)
# least squares solution =  11.903836730738725  +/-  0.013045474123784755

#  2024-02-25 19:58:19.338994
# source:  /Volumes/T7-Touch/repos/github/jop/python/dtra/taylor/fireball-01.py
# user id: dantopa
# platform info:
#     platform:  macOS-14.2.1-x86_64-i386-64bit
#     uname:     uname_result(system='Darwin', node='Quaxolotl.local', release='23.2.0', version='Darwin Kernel Version 23.2.0: Wed Nov 15 21:54:10 PST 2023; root:xnu-10002.61.3~2/RELEASE_X86_64', machine='x86_64')
# version info:
#     python:   3.9.6 (default, Dec  7 2023, 05:42:47) 
# [Clang 15.0.0 (clang-1500.1.0.2.5)]
#     numpy:    1.26.2
#     platform: 1.0.8

