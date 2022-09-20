#! /opt/local/bin/python
from datetime import date
today = date.today( )
print( today.strftime("%b-%d-%Y") )
import os
print(os.path.dirname(os.path.realpath(__file__)))

# https://www.youtube.com/watch?v=eTucYT2LpNU
import math
answer = math.factorial(10000)
print(f"{answer=:x}")
