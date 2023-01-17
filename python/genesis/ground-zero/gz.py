#! /opt/local/bin/python
#! /home/dantopa/spacktivity/ubuntu-22.04-dantopa-docker-spack/opt/spack/linux-ubuntu22.04-haswell/gcc-12.2.0/python-3.10.6-ybcookynohghdr6i72gwalqle6hq27z5/bin/python
# Solving Bevington example 6.1 with Python
import datetime             # timestamps
import os                   # opeating system
import sys                  # python version

print( "importing numpy..." )
import numpy as np

# input data
x     = np.array( [  1, 20, 50 ] );
y     = np.array( [ 66, 15, -3 ] );
theta = np.array( [ 1.0, 0.74, 0.43 ] );

# data vectors
c = np.cos( theta );
s = np.sin( theta );

# form linear system Ax = b
A = np.transpose( [ c, -s ] )
print( "design matrix A = \n", np.matrix( A ) )
b = np.multiply( x, c ) - np.multiply( y, s )
print ( "data vector b =", np.matrix( b ))

# inner products
cc = np.dot(c, c);
cs = np.dot(c, s);
ss = np.dot(s, s);
cb = np.dot(c, b);
sb = np.dot(s, b);

det = cc * ss - cs**2

# normal equations solution
Winv = np.array( [ [ ss, cs ], [ cs, cc ] ] ) / det;
atb  = np.array( [ cb, -sb ] );
xls  = np.dot( Winv, atb );
print ( "least squares solution xls =", xls )

# error propagation
residual = np.dot( A, xls ) - b
t2 = np.dot( residual, residual )
print( "least total squared error =", t2 )
[ m, n ] = A.shape
print( "A matrix dimensions =", [ m, n ] )
diag  = np.diag( Winv )
sigma = np.sqrt( t2 / ( m - n ) * diag )
print ( "sigma =", sigma )

# compare to mathematica
xlsExact   = [ 117.97723925949964161745199905235647691501049017468,
               135.24677447077613795832279777569468400355063639720 ];
sigmaExact = [ 18.698052680295699237828157411268853967898756424020,
               20.860166494699188800182633692615600495039424579191 ];

numericErrorXLS   = xls - xlsExact
numericErrorSigma = sigma - sigmaExact

# machine epsilon
machineEpsilon = np.finfo(float).eps
print( "\nmachine epsilon =", np.finfo(float).eps )
numericErrorXLSeps   = numericErrorXLS   / machineEpsilon
numericErrorXLSsigma = numericErrorSigma / machineEpsilon
print( "\nnumeric epsilons, fit parameters:   ", numericErrorXLSeps )
print( "\nnumeric epsilons, sigma parameters: ", numericErrorXLSsigma )

print( "particular least squares solution for ground zero\n" )
print( "x0 = %f +/- %f", %( xls( 1 ), sigma( 1 ) ) )
# print( "y0 = %4.15f +/- %4.15f\n", xls( 2 ), sigma( 2 ) )


#   farewell with provenance
print( "\n", datetime.datetime.now( ) )
print( "source: %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
print( "python version %s" % sys.version )


# dantopa@Quaxolotl.local:ground-zero $ python gz.py
# Jan-16-2023
# /Volumes/T7-Touch/repos/github/jop/python/genesis/ground-zero
# importing numpy...
# design matrix A =
#  [[ 0.54030231 -0.84147098]
#  [ 0.73846856 -0.67428791]
#  [ 0.90896575 -0.4168708 ]]
# data vector b = [[-54.99678269   4.6550525   46.69889989]]
# least squares solution xls = [117.97723926 135.24677447]
# least total squared error = 117.80714180203773
# A matrix dimensions = [3, 2]
# sigma = [18.69805268 20.86016649]
