#! /opt/local/bin/python
#! /home/dantopa/spacktivity/ubuntu-22.04-dantopa-docker-spack/opt/spack/linux-ubuntu22.04-haswell/gcc-12.2.0/python-3.10.6-ybcookynohghdr6i72gwalqle6hq27z5/bin/python
#! /home/dantopa/spacktivity/ubuntu-22.04-dantopa-docker-spack/opt/spack/linux-ubuntu22.04-haswell/gcc-12.2.0/python-3.10.6-ybcookynohghdr6i72gwalqle6hq27z5/bin
# Solving Bevington example 6.1 with Julia
print( "importing numpy..." )
import numpy as np
A = np.array([ [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 8], [1, 9] ])
print( "design matrix A\n", np.matrix( A ) )
T = np.array([15.6, 17.5, 36.6, 43.8, 58.2, 61.6, 64.2, 70.4, 98.8])
print ( "data vector T\n", np.matrix( T ))
W = np.dot( A.transpose(), A )
print( "Gram matrix A*A\n", np.matrix( W ) )
b = np.dot( A.transpose(), T )
print( "least squares solution" )
xls = np.linalg.solve( W, b )
print ( "least squares solution xls\n", xls )

# dantopa@Quaxolotl.attlocal.net:least-squares $ date
# Mon Sep  5 12:55:15 CDT 2022

# dantopa@Quaxolotl.attlocal.net:least-squares $ pwd
# /Volumes/T7-Touch/repos/github/jop/python/genesis/least-squares

# dantopa@Quaxolotl.attlocal.net:least-squares $ ./least-squares.py
# importing numpy
# input design matrix
# input data vector
# construct Gram matrix
# least squares solution
# [[1 1]
#  [1 2]
#  [1 3]
#  [1 4]
#  [1 5]
#  [1 6]
#  [1 7]
#  [1 8]
#  [1 9]]
#
