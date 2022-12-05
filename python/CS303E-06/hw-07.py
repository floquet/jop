#! /opt/local/bin/python
# CS303E Homework
from datetime import date
import math
import os
today = date.today( )
print( today.strftime("%b-%d-%Y") )
print(os.path.dirname(os.path.realpath(__file__)))

HW_ERROR_MESSAGE = "Grade must be in range [0..10]. Try again."

print( "Average three grades" )
def computeHomeworkAvg(hw1, hw2, hw3):
    while (hw1 < 0 or hw1 > 10):
        print( "hw1 = ", hw1 )
        print( HW_ERROR_MESSAGE )
        hw1 = int(input( "  Enter HW1 grade =  " ))
    while (hw2 < 0 or hw2 > 10):
        print( "hw2 = ", hw2 )
        print( HW_ERROR_MESSAGE )
        hw2 = int(input( "  Enter HW2 grade =  " ))
    while (hw3 < 0 or hw3 > 10):
        print( "hw3 = ", hw3 )
        print( HW_ERROR_MESSAGE )
        hw3 = int(input( "  Enter HW3 grade =  " ))
    ave = ( hw1 + hw2 + hw3 ) / 3
    print( "average of hw scores = ", ave)
    return ave;

# Test the program using an expected answer
hw1 = 1
hw2 = 2
hw3 = 3
expected = 2
result = computeHomeworkAvg (hw1, hw2, hw3)

print( "expected average = ", expected )
print( "computed average = ", result )
print( "expected == computed? ", result==expected )


# Test using bad values
hw1 = -1
hw2 = 2
hw3 = 3
result = computeHomeworkAvg (hw1, hw2, hw3)

# Test using bad values
hw1 = 1
hw2 = -2
hw3 = 3
result = computeHomeworkAvg (hw1, hw2, hw3)

# Test using bad values
hw1 = 1
hw2 = 2
hw3 = -3
result = computeHomeworkAvg (hw1, hw2, hw3)

# $ python hw-07.py
# Oct-10-2022
# /Volumes/T7-Touch/repos/github/jop/python/CS303E-06
# Average three grades
# average of hw scores =  2.0
# expected average =  2
# computed average =  2.0
# expected == computed?  True
# hw1 =  -1
# Grade must be in range [0..10]. Try again.
#   Enter HW1 grade =  1
# average of hw scores =  2.0
# hw2 =  -2
# Grade must be in range [0..10]. Try again.
#   Enter HW2 grade =  2
# average of hw scores =  2.0
# hw3 =  -3
# Grade must be in range [0..10]. Try again.
#   Enter HW3 grade =  3
# average of hw scores =  2.0
