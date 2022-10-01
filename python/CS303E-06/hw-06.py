#! /opt/local/bin/python
# CS303E Homework 6
# https://www.cs.utexas.edu/~byoung/cs303e/hw6.html

from datetime import date
import math
import os
today = date.today( )
print( today.strftime("%b-%d-%Y") )
print(os.path.dirname(os.path.realpath(__file__)))

# 1. Write a function to return the sum of three numbers.
print( "\n (1)" )
def sum3Numbers (x, y, z):
    return x + y + z;

x = 1
y = 2
z = 3
expected = 6
result = sum3Numbers (x, y, z)

print( "sum the numbers ", x, ", ", y, ", ", z, ": expected answer = ", expected )
print( "sum3Numbers (", x, ", ", y, ", ", z, ") = ", sum3Numbers (x, y, z) )
print( "did we get expected answer? ", result==expected )

# 2. Write a function to return the product of three numbers.
print( "\n (2)" )
def multiply3Numbers (x, y, z):
    return x * y * z;

x = 1
y = 2
z = 3
expected = 6
result = multiply3Numbers (x, y, z)

print( "multiply the numbers ", x, ", ", y, ", ", z, ": expected answer = ", expected )
print( "multiply3Numbers (", x, ", ", y, ", ", z, ") = ", multiply3Numbers (x, y, z) )
print( "did we get expected answer? ", result==expected )

# 3. Write a function to return the sum of up to 3 numbers.  It should
#    accept 1, 2, or 3 parameters.  Hint: any parameter not given
#    should default to 0.
print( "\n (3): sum up to three" )
def sumUpTo3Numbers ( x, y = 0, z = 0 ):
    if y == 0:
        return x
    if z == 0:
        return x + y;
    return sum3Numbers (x, y, z);

x = 5
y = 0
z = 0
expected = 5
result = sumUpTo3Numbers (x, y, z)

print( "\ncase a")
print( "multiply the numbers ", x, ", ", y, ", ", z, ": expected answer = ", expected )
print( "sumUpTo3Numbers (", x, ", ", y, ", ", z, ") = ", sumUpTo3Numbers (x, y, z) )
print( "did we get expected answer? ", result==expected )

x = 5
y = 6
z = 0
expected = 11
result = sumUpTo3Numbers (x, y, z)

print( "\ncase b")
print( "multiply the numbers ", x, ", ", y, ", ", z, ": expected answer = ", expected )
print( "sumUpTo3Numbers (", x, ", ", y, ", ", z, ") = ", sumUpTo3Numbers (x, y, z) )
print( "did we get expected answer? ", result==expected )

x = 5
y = 6
z = 7
expected = 18
result = sumUpTo3Numbers (x, y, z)

print( "\ncase c")
print( "multiply the numbers ", x, ", ", y, ", ", z, ": expected answer = ", expected )
print( "sumUpTo3Numbers (", x, ", ", y, ", ", z, ") = ", sumUpTo3Numbers (x, y, z) )
print( "did we get expected answer? ", result==expected )

# 4. Write a function to return the product of up to 3 numbers.  It
#    should accept 1, 2, or 3 parameters.  Hint: what should the
#    default be in this case?
print( "\n (4): multiply up to three" )
def multiplyUpTo3Numbers ( x, y = 1, z = 1 ):
    if y == 1:
        return x
    if z == 1:
        return x * y;
    return multiply3Numbers (x, y, z);

x = 5
y = 1
z = 1
expected = 5
result = multiplyUpTo3Numbers (x, y, z)

print( "\ncase a")
print( "multiply the numbers ", x, ", ", y, ", ", z, ": expected answer = ", expected )
print( "multiplyUpTo3Numbers (", x, ", ", y, ", ", z, ") = ", multiplyUpTo3Numbers (x, y, z) )
print( "did we get expected answer? ", result==expected )

x = 5
y = 6
z = 1
expected = 30
result = multiplyUpTo3Numbers (x, y, z)

print( "\ncase b")
print( "multiply the numbers ", x, ", ", y, ", ", z, ": expected answer = ", expected )
print( "multiplyUpTo3Numbers (", x, ", ", y, ", ", z, ") = ", multiplyUpTo3Numbers (x, y, z) )
print( "did we get expected answer? ", result==expected )

x = 5
y = 6
z = 7
expected = 210
result = multiplyUpTo3Numbers (x, y, z)

print( "\ncase c")
print( "multiply the numbers ", x, ", ", y, ", ", z, ": expected answer = ", expected )
print( "multiplyUpTo3Numbers (", x, ", ", y, ", ", z, ") = ", multiplyUpTo3Numbers (x, y, z) )
print( "did we get expected answer? ", result==expected )

# 5. Write a function that takes 2 numbers as input and prints them
#    out in ascending order.
print( "\n (5): print numbers in order" )

def printInOrder( x, y ):
    if x >= y:
        print( "x >= y: larger = ", x, ", smaller = ", y)
        return;
    if x < y:
        print( "x < y: larger = ", y, ", smaller = ", x)
        return;
    print( "program error: perhaps we are not comparing numbers?")
    return;

x = 5
y = 6
print( "\nexpected output: ", y, ", ", x )
printInOrder (x, y)

x = 5
y = -11
print( "\nexpected output: ", x, ", ", y)
printInOrder (x, y)

# 6. Write a function that returns the area of a square, given the length of a side.
#    Print an error message if side is negative.
print( "\n (6): area of square" )
def areaOfSquare( side ):
    if side < 0:
        print( "\nwhoops! negative side length = ", side );
        return;
    return side**2;

side = 3.3
expected = side * side;
result = areaOfSquare ( side );
print( "length of side = ", side, ": expected area = ", expected )
print( "areaOfSquare (", side, ") = ", result )
print( "did we get expected answer? ", result==expected )

side = -1
result = areaOfSquare ( side );
print( "length of side = ", side )
print( "expect error message" )

# 7. Write a function that returns the perimeter of a square, given
#    the length of a side.  Print an error message if side is negative.
print( "\n (7): perimeter of a square" )
def perimeterOfSquare( side ):
    if side < 0:
        print( "\nwhoops! negative side length = ", side );
        return;
    return 4 * side;

side = 3.3
expected = 4 * side;
result = perimeterOfSquare ( side );
print( "length of side = ", side, ": expected perimeter = ", expected )
print( "perimeterOfSquare (", side, ") = ", result )
print( "did we get expected answer? ", result==expected )

side = -1
result = areaOfSquare ( side );
print( "length of side = ", side )
print( "expect error message" )
areaOfSquare ( side )

# 8. Write a function that returns the area of a circle, given the
#    radius.  Use math.pi. Print an error message if radius is negative.
print( "\n (8): area of a circle" )
def areaOfCircle( radius ):
    if radius < 0:
        print( "\nwhoops! negative radius = ", radius );
        return;
    return math.pi * radius**2;

radius = 3.3
expected = math.pi * radius**2;
result = areaOfCircle ( radius );
print( "\nradius = ", radius, ": expected area = ", expected )
print( "areaOfCircle (", radius, ") = ", result )
print( "did we get expected answer? ", result==expected )

radius = -1
areaOfCircle ( radius )
print( "radius = ", radius )
print( "expect error message" )

# 9. Write a function that returns the circumference of a circle given
#    the radius.  Use math.pi. Print an error if radius is negative.
print( "\n (9): perimeter of a circle" )
def circumferenceOfCircle( radius ):
    if radius < 0:
        print( "\nwhoops! negative radius = ", radius );
        return;
    return 2 * math.pi * radius;

radius = 3.3
expected = 2 * math.pi * radius;
result = circumferenceOfCircle ( radius );
print( "\nradius = ", radius, ": expected area = ", expected )
print( "circumferenceOfCircle (", radius, ") = ", result )
print( "did we get expected answer? ", result==expected )

radius = -1
circumferenceOfCircle ( radius )
print( "radius = ", radius )
print( "expect error message" )

# 10. Write a function: given parameters d1, d2, x, returns whether
#    both d1 and d2 are both factors (evenly divide) x.  You can
#    assume all values are integers.
print( "\n (10): integer factors" )
def bothFactors( d1, d2, x ):
    if x%d1==0:
        print( "d1 = ", d1, " is a factor of x = ", x );
        print( "x / d1 = ", x / d1 );
    else:
        print( "d1 = ", d1, " is NOT a factor of x = ", x );
    if x%d2==0:
        print( "d2 = ", d2, " is a factor of x = ", x );
        print( "x / d2 = ", x / d2 );
    else:
        print( "d2 = ", d2, " is NOT a factor of x = ", x );
    return;

x = 39916800; # 17! = 1 * 2 * 3 * ... * 16 * 17
d1 = 7;
d2 = 19;
print( "\nx = ", x, " = 17!" )
print( "is d1 = ", d1, " a factor of 17!: YES")
print( "is d2 = ", d2, " a factor of 17!: NO")
bothFactors( d1, d2, x )

# 11. Given a value x, compute and print out the area and circumference of a circle with
#    radius x and the area and perimeter of a square with side x.  Use your previous
#    functions for these computations.  Leave a blank line above and below the printing.
def squareAndCircle( x ):
print( "\n (11): compute and print out the area and circumference of a circle" )

radius = 2.2;
side = 1.1;
expectedCircumference = 2 * math.pi * radius;
resultCircumference = circumferenceOfCircle( radius )
expectedArea = math.pi * radius^2;
resultArea = circumferenceOfCircle( radius )

print( "\n radius = ", radius )
print( "circumference = ", circumferenceOfCircle( radius ) )
print( "area = \n", areadOfCircle( radius ) )

# $ python hw-06.py
# Sep-30-2022
# /Volumes/T7-Touch/repos/github/jop/python/CS303E-06
#
#  (1)
# sum the numbers  1 ,  2 ,  3 : expected answer =  6
# sum3Numbers ( 1 ,  2 ,  3 ) =  6
# did we get expected answer?  True
#
#  (2)
# multiply the numbers  1 ,  2 ,  3 : expected answer =  6
# multiply3Numbers ( 1 ,  2 ,  3 ) =  6
# did we get expected answer?  True
#
#  (3): sum up to three
#
# case a
# multiply the numbers  5 ,  0 ,  0 : expected answer =  5
# sumUpTo3Numbers ( 5 ,  0 ,  0 ) =  5
# did we get expected answer?  True
#
# case b
# multiply the numbers  5 ,  6 ,  0 : expected answer =  11
# sumUpTo3Numbers ( 5 ,  6 ,  0 ) =  11
# did we get expected answer?  True
#
# case c
# multiply the numbers  5 ,  6 ,  7 : expected answer =  18
# sumUpTo3Numbers ( 5 ,  6 ,  7 ) =  18
# did we get expected answer?  True
#
#  (4): multiply up to three
#
# case a
# multiply the numbers  5 ,  1 ,  1 : expected answer =  5
# multiplyUpTo3Numbers ( 5 ,  1 ,  1 ) =  5
# did we get expected answer?  True
#
# case b
# multiply the numbers  5 ,  6 ,  1 : expected answer =  30
# multiplyUpTo3Numbers ( 5 ,  6 ,  1 ) =  30
# did we get expected answer?  True
#
# case c
# multiply the numbers  5 ,  6 ,  7 : expected answer =  210
# multiplyUpTo3Numbers ( 5 ,  6 ,  7 ) =  210
# did we get expected answer?  True
#
#  (5): print numbers in order
#
# expected output:  6 ,  5
# x < y: larger =  6 , smaller =  5
#
# expected output:  5 ,  -11
# x >= y: larger =  5 , smaller =  -11
#
#  (6): area of square
# length of side =  3.3 : expected area =  10.889999999999999
# areaOfSquare ( 3.3 ) =  10.889999999999999
# did we get expected answer?  True
#
# whoops! negative side length =  -1
# length of side =  -1
# expect error message
#
#  (7): perimeter of a square
# length of side =  3.3 : expected perimeter =  13.2
# perimeterOfSquare ( 3.3 ) =  13.2
# did we get expected answer?  True
#
# whoops! negative side length =  -1
# length of side =  -1
# expect error message
#
# whoops! negative side length =  -1
#
#  (8): area of a circle
#
# radius =  3.3 : expected area =  34.21194399759284
# areaOfCircle ( 3.3 ) =  34.21194399759284
# did we get expected answer?  True
#
# whoops! negative radius =  -1
# radius =  -1
# expect error message
#
#  (9): perimeter of a circle
#
# radius =  3.3 : expected area =  20.734511513692635
# circumferenceOfCircle ( 3.3 ) =  20.734511513692635
# did we get expected answer?  True
#
# whoops! negative radius =  -1
# radius =  -1
# expect error message
#
#  (10): integer factos
#
# x =  39916800  = 17!
# is d1 =  7  a factor of 17!: YES
# is d2 =  19  a factor of 17!: NO
# d1 =  7  is a factor of x =  39916800
# x / d1 =  5702400.0
# d2 =  19  is NOT a factor of x =  39916800
