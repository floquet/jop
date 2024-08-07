#! /opt/local/bin/python
#! /home/dantopa/spacktivity/ubuntu-22.04-dantopa-docker-spack/opt/spack/linux-ubuntu22.04-haswell/gcc-12.2.0/python-3.10.6-ybcookynohghdr6i72gwalqle6hq27z5/bin/python
# Solving Bevington example 6.1 with Python
import datetime             # timestamps
import numpy as np 			# array operations
import os                   # opeating system
import sys                  # python version

# The Formation of a Blast Wave by a Very Intense Explosion II. The Atomic Explosion of 1945
# Geoffrey Ingram Taylor
# Table 1, p. 176
# time: s
# radius: cm
t = np.array( [ 0.0001, 0.00024, 0.00038, 0.00052, 0.00066, 0.0008, 0.00094, 0.00108, 0.00122, 0.00136, 0.0015, 0.00165, 0.00179, 0.00193, 0.00326, 0.00353, 0.0038, 0.00407, 0.00434, 0.00461, 0.015, 0.025, 0.034, 0.053, 0.062 ] )
r = np.array( [ 1110., 1990., 2540., 2880., 3190., 3420., 3630., 3890., 4100., 4280., 4440., 4600., 4690., 4870., 5900., 6110., 6290., 6430., 6560., 6730., 10650., 13000., 14500., 17500., 18500. ] )
# print ( "observation times t =", np.matrix( t ) )
#m = np.ndarray.size( t )
m = t.size
print ( "m = ", m ) 

# p. 178
rhoTaylor  = 0.00125
gamma      = 1.4
# U.S. Standard atmosphere for 1500 m elevation
rhoTrinity = 0.00105807

# Table 3, p. 180
I1 = 0.185
I2 = 0.187
# Energy partition - kinetic + potential
# (7) p. 178
K = 2 * math.pi * I1
K = K + 4 * np.pi * I2 / gamma / ( gamma - 1 )
K = 4 * K / 25

# logarithmic transforms
x =         np.log10( t )
y = 5 / 2 * np.log10( r )

# least squares solution for intercept a0
a0 = np.average( y ) - np.average( x )
print ( "K =", K )
print ( "a0 =", a0 )

residualV = a0 - y + x
t2 = np.dot( residualV, residualV )
print ( "t2 = ", t2 ) 
sigma = np.sqrt( t2 / m / (m - 1) )
print ( "least squares solution = ", a0, " +/- ", sigma ) 


#   farewell with provenance
print( "\n", datetime.datetime.now( ) )
print( "source: %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
print( "python version %s" % sys.version )

