#! /opt/local/bin/python
#! /home/dantopa/spacktivity/ubuntu-22.04-dantopa-docker-spack/opt/spack/linux-ubuntu22.04-haswell/gcc-12.2.0/python-3.10.6-ybcookynohghdr6i72gwalqle6hq27z5/bin/python
# Solving Bevington example 6.1 with Python
from datetime import date
today = date.today( )
print( today.strftime("%b-%d-%Y") )
import os
print(os.path.dirname(os.path.realpath(__file__)))

print( "\ndefining membership lists" )
listIAC = [ "John", "Jarret", "Bill", "Dan" ]
listASD = [ "John", "Diana", "Paul" ]

print( "\nprint membership lists" )
print( "Who is in IAC?: ", listIAC)
print( "Who is in ASD?: ", listASD)

print( "\npboolean operations" )
print( "Who is in IAC and ASD?: ", listIAC and listASD )
print( "Who is in both IAC and ASD?: ", listIAC or listASD )
