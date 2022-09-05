#! /opt/local/bin/python
#! /home/dantopa/spacktivity/ubuntu-22.04-dantopa-docker-spack/opt/spack/linux-ubuntu22.04-haswell/gcc-12.2.0/python-3.10.6-ybcookynohghdr6i72gwalqle6hq27z5/bin/python
# Solving Bevington example 6.1 with Julia
print( "importing numpy..." )
import numpy as np

# input data
A = np.array([ [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9] ])
print( "design matrix A\n", np.matrix( A ) )
T = np.array([15.6, 17.5, 36.6, 43.8, 58.2, 61.6, 64.2, 70.4, 98.8])
print ( "data vector T =", np.matrix( T ))

# set up normal equations
W = np.dot( A.transpose(), A )
print( "Gram matrix A*A\n", np.matrix( W ) )
b = np.dot( A.transpose(), T )

# solve normal equations
xls = np.linalg.solve( W, b )
print ( "least squares solution xls =", xls )

# pseudoinverse solution
Winv  = np.linalg.inv( W )
Ap    = np.dot( Winv, A.transpose( ) )
xpinv = np.dot( Ap, T.transpose( ) )
print( "pseudoinverse         xpinv =", xpinv )

# dantopa@Quaxolotl.attlocal.net:least-squares $ ./least-squares.py
# importing numpy...
# design matrix A
#  [[1 1]
#  [1 2]
#  [1 3]
#  [1 4]
#  [1 5]
#  [1 6]
#  [1 7]
#  [1 8]
#  [1 9]]
# data vector T = [[15.6 17.5 36.6 43.8 58.2 61.6 64.2 70.4 98.8]]
# Gram matrix A*A
#  [[  9  45]
#  [ 45 285]]
# least squares solution xls = [4.81388889 9.40833333]
