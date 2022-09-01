# Solving Bevington example 6.1 with Julia
printf( "Bevington Example 6.1\n" )
strftime ("%Y-%m-%d %H:%M:%S", localtime (time ()))

# design matrix
A = [ 1 1; 1 2; 1 3; 1 4; 1 5; 1 6; 1 7; 1 8; 1 9 ];
A
disp(A)

# Define data
x = [ 1; 2; 3; 4; 5; 6; 7; 8; 9 ];
T = [ 78/5; 35/2; 183/5; 219/5; 291/5; 308/5; 321/5; 352/5; 494/5 ];
T

# solve least squares problem
xls = A \ T;
xls

# error analysis

# residual error vector
residual = A * xls - T;
t2 = dot( residual, residual );

# compute Gram matrix
W = transpose( A ) * A
Winv = inv( W )
values = diag( Winv )

# m = rows, n = columns
[ m, n ] = size ( A );
g = sprintf('%d ', [ m, n ]);
fprintf('matrix dimensions: %s\n', g);

sigma = sqrt( t2 / ( m - n ) * values )

## dantopa@Quaxolotl.local:least-squares $ octave-cli boo.m
## ans = 2022-08-31 18:16:17
## A =
##
##    1   1
##    1   2
##    1   3
##    1   4
##    1   5
##    1   6
##    1   7
##    1   8
##    1   9
