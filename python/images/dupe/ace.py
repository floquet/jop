#! /opt/local/bin/python
#! /home/dantopa/spacktivity/ubuntu-22.04-dantopa-docker-spack/opt/spack/linux-ubuntu22.04-haswell/gcc-12.2.0/python-3.10.6-ybcookynohghdr6i72gwalqle6hq27z5/bin/python
# Solving Bevington example 6.1 with Python
from datetime import date
today = date.today( )
print( today.strftime("%b-%d-%Y") )
import os
print(os.path.dirname(os.path.realpath(__file__)))

print( "importing numpy..." )
import numpy as np


#   farewell with provenance
print( "\n", datetime.datetime.now( ) )
print( "source: %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
print( "python version %s" % sys.version )
