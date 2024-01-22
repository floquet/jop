#! /opt/local/bin/python
#! /home/dantopa/spacktivity/ubuntu-22.04-dantopa-docker-spack/opt/spack/linux-ubuntu22.04-haswell/gcc-12.2.0/python-3.10.6-ybcookynohghdr6i72gwalqle6hq27z5/bin/python
# Solving Bevington example 6.1 with Python
from datetime import date, datetime
# import datetime
today = date.today( )
print( today.strftime("%b-%d-%Y") )
import os
print(os.path.dirname(os.path.realpath(__file__)))

print( "importing numpy..." )
import numpy as np

# from scipy.optimize import fmin
from scipy.optimize import least_squares


# input data
R = np.array([ 1110, 1990, 2540, 2880, 3190, 3420, 3630, 3890, 4100, 4280, \
4440, 4600, 4690, 4870, 5900, 6110, 6290, 6430, 6560, 6730, 10650, 13000, 14500, 17500, 18500 ])
print( "data vector R\n", np.matrix( R ) )
T = np.array([0.0001, 0.00024, 0.00038, 0.00052, 0.00066, 0.0008, 0.00094, 0.00108, 0.00122, 0.00136, 0.0015, 0.00165, 0.00179, 0.00193, \
0.00326, 0.00353, 0.0038, 0.00407, 0.00434, 0.00461, 0.015, 0.025, 0.034, 0.053, 0.062])
print ( "mesh vector T =", np.matrix( T ))

# logarithms
y = 5 / 2 * np.log10( R )
x =         np.log10( T )

# compute mean
ybar = np.mean( y )
xbar = np.mean( x )

# intercept
a0 = ybar - xbar
# Xi R^{5} t^{-2}
Xi = np.power( 10, 2 * a0 )
print ( "a0 =", a0 )
print ( "Xi =", Xi )
print ( "np.power( T, b ) = ", np.power( T, 1 ) )

# nonlinear solution
def phi( a, b ):
	return np.linalg.norm( a * np.power( T, b ) - R )

print ( "phi( 54474, 0.388301 ) =", phi( 54474, 0.388301 ) )
print ( "phi( 1, 0.1 ) =", phi( 1, 1 ) )

soln = scipy.optimize.least_squares( phi, method='lm', args = (a, b) )
print ( "soln =", soln )


#   farewell with provenance
#print( "\n", datetime.datetime.now( ) )
print( "source: %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
#print( "python version %s" % sys.version )
