#! /opt/local/bin/python
#! /home/dantopa/spacktivity/ubuntu-22.04-dantopa-docker-spack/opt/spack/linux-ubuntu22.04-haswell/gcc-12.2.0/python-3.10.6-ybcookynohghdr6i72gwalqle6hq27z5/bin/python
# Solving Bevington example 6.1 with Python
import datetime             # timestamps
import os                   # opeating system
import sys                  # python version

print( "importing numpy..." )
import numpy as np
np.set_printoptions(precision=17, floatmode='unique')

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

print ( "particular least squares solution for ground zero" )
print ( "x0 =", xls[ 0 ], "+/-", sigma[ 0 ] )
print ( "y0 =", xls[ 1 ], "+/-", sigma[ 1 ] )

# compare to mathematica
xlsExact   = [ 117.97723925949964161745199905235647691501049017468,
               135.24677447077613795832279777569468400355063639720 ];
sigmaExact = [ 18.698052680295699237828157411268853967898756424020,
               20.860166494699188800182633692615600495039424579191 ];

numericErrorXLS   = xls - xlsExact
numericErrorSigma = sigma - sigmaExact

# machine epsilon
machineEpsilon = np.finfo(float).eps
numericErrorXLSeps   = numericErrorXLS   / machineEpsilon
numericErrorXLSsigma = numericErrorSigma / machineEpsilon
print( "\n Errors in machine epsilon =", np.finfo(float).eps )

print ( "x0 =", numericErrorXLSeps[ 0 ], "+/-", numericErrorXLSsigma[ 0 ] )
print ( "y0 =", numericErrorXLSeps[ 1 ], "+/-", numericErrorXLSsigma[ 1 ] )


#   farewell with provenance
print( "\n", datetime.datetime.now( ) )
print( "source: %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
print( "python version %s" % sys.version )


# importing numpy...
# design matrix A = 
#  [[ 0.5403023058681398  -0.8414709848078965 ]
#  [ 0.7384685587295879  -0.674287911628145  ]
#  [ 0.9089657496748851  -0.41687080242921076]]
# data vector b = [[-54.99678269145303     4.6550525001695835  46.698899891031886 ]]
# least squares solution xls = [117.97723925949958 135.2467744707761 ]
# least total squared error = 117.80714180203773
# A matrix dimensions = [3, 2]
# sigma = [18.698052680295692 20.860166494699182]
# particular least squares solution for ground zero
# x0 = 117.97723925949958 +/- 18.698052680295692
# y0 = 135.2467744707761 +/- 20.860166494699182
# 
#  Errors in machine epsilon = 2.220446049250313e-16
# x0 = -256.0 +/- -32.0
# y0 = -128.0 +/- -32.0
# 
#  2024-05-29 15:54:41.289181
# source: /Volumes/T7-Touch/repos/github/jop/python/genesis/ground-zero/gz2.py
# python version 3.12.3 (main, Apr 12 2024, 20:23:48) [Clang 15.0.0 (clang-1500.1.0.2.5)]
