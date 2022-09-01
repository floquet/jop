# Solving Bevington example 6.1 with Julia
printf( "Bevington Example 6.1\n" )
strftime ("%Y-%m-%d %H:%M:%S", localtime (time ()))

# design matrix
A = [ 1 1; 1 2; 1 3; 1 4; 1 5; 1 6; 1 7; 1 8; 1 9 ];
printf( "design matrix:\n" )
A
# disp(A)

# Define data
x = [ 1; 2; 3; 4; 5; 6; 7; 8; 9 ];
#T = [ 78/5; 35/2; 183/5; 219/5; 291/5; 308/5; 321/5; 352/5; 494/5 ];
T = [15.6; 17.5; 36.6; 43.8; 58.2; 61.6; 64.2; 70.4; 98.8];
printf( "data vector:\n" )
T

# solve least squares problem
xls = A \ T;
printf( "least squares solution\n" )
printf( "xls = A \\ T:\n" )
xls

# error analysis

# residual error vector
residual = A * xls - T;
printf( "residual error vector\n" )
printf( "residual = A * xls - T:\n" )

t2 = dot( residual, residual );
printf( "least total squared error\n" )
printf( "t2 = residual . residual :\n" )
t2

# compute Gram matrix
W = transpose( A ) * A
printf( "compute Gram matrix\n" )
printf( "W = transpose( A ) * A\n" )

Winv = inv( W )
printf( "invert Gram matrix\n" )
printf( "Winv = inv( W )\n" )
Winv

values = diag( Winv )
printf( "harvest diagonal elements of Winv" )
printf( "values = diag( Winv ):\n" )
values

# measure design matrix
# m = rows, n = columns
[ m, n ] = size ( A );
g = sprintf('%d ', [ m, n ]);
fprintf('matrix dimensions: %s\n', g);

sigma = sqrt( t2 / ( m - n ) * values );
printf( "compute error elements:\n" )
printf( "sigma = sqrt( t2 / ( m - n ) * values ):\n" )
sigma

printf( "\n#  #  #  Compare Octave values to exact values\n" )
printf( "\nFit parameters\n" )

numericError = xls - [ 1733 / 360; 1129 / 120 ];
printf( "\nerror in intercept and slope values\n" )
printf( "numericError = xls - [ 1733 / 360; 1129 / 120 ]\n" )
numericError

epsError = numericError ./ eps( 1.0 );
printf( "\nerror in intercept and slope values in machine epsilon\n" )
printf( "epsError = numericError ./ eps( 1.0 )\n" )
epsError

printf( "\nError parameters\n" )
numericError = sigma - sqrt( [ 108297055; 3419907 ] / 35 ) / 360;
printf( "\nintercept and slope sigmas\n" )
printf( "numericError = sigma - sqrt( [ 108297055; 3419907 ] / 35 ) / 360\n" )
numericError

epsError = numericError ./ eps( 1.0 );
printf( "\nerror in intercept and slope sigmas in machine epsilon\n" )
printf( "epsError = numericError ./ eps( 1.0 )\n" )
epsError

output_precision(16)
printf( "\noutput_precision(16)\n" )
xls
sigma

// /Volumes/T7-Touch/repos/github/jop/octave/genesis/least-squares
// dantopa@Quaxolotl.local:least-squares $ octave-cli least-squares.m
// Bevington Example 6.1
// ans = 2022-09-01 05:22:36
// design matrix:
// A =
//
//    1   1
//    1   2
//    1   3
//    1   4
//    1   5
//    1   6
//    1   7
//    1   8
//    1   9
//
// data vector:
// T =
//
//    15.600
//    17.500
//    36.600
//    43.800
//    58.200
//    61.600
//    64.200
//    70.400
//    98.800
//
// least squares solution
// xls = A \ T:
// xls =
//
//    4.8139
//    9.4083
//
// residual error vector
// residual = A * xls - T:
// least total squared error
// t2 = residual . residual :
// t2 = 316.66
// W =
//
//      9    45
//     45   285
//
// compute Gram matrix
// W = transpose( A ) * A
// Winv =
//
//    0.527778  -0.083333
//   -0.083333   0.016667
//
// invert Gram matrix
// Winv = inv( W )
// Winv =
//
//    0.527778  -0.083333
//   -0.083333   0.016667
//
// values =
//
//    0.527778
//    0.016667
//
// harvest diagonal elements of Winvvalues = diag( Winv ):
// values =
//
//    0.527778
//    0.016667
//
// matrix dimensions: 9 2
// compute error elements:
// sigma = sqrt( t2 / ( m - n ) * values ):
// sigma =
//
//    4.8862
//    0.8683
//
//
// #  #  #  Compare Octave values to exact values
//
// Fit parameters
//
// error in intercept and slope values
// numericError = xls - [ 1733 / 360; 1129 / 120 ]
// numericError =
//
//   -1.0658e-14
//    1.7764e-15
//
//
// error in intercept and slope values in machine epsilon
// epsError = numericError ./ eps( 1.0 )
// epsError =
//
//   -48
//     8
//
//
// Error parameters
//
// intercept and slope sigmas
// numericError = sigma - sqrt( [ 108297055; 3419907 ] / 35 ) / 360
// numericError =
//
//    8.8818e-16
//    1.1102e-16
//
//
// error in intercept and slope sigmas in machine epsilon
// epsError = numericError ./ eps( 1.0 )
// epsError =
//
//    4.0000
//    0.5000
//
//
// output_precision(16)
// xls =
//
//    4.813888888888878
//    9.408333333333335
//
// sigma =
//
//    4.886206312183355
//    0.868301647656361
//
