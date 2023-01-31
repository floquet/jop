# Ground zero from bearing angles

printf( "Finding ground zero with bearing angles\n" )
strftime ("%Y-%m-%d %H:%M:%S", localtime (time ()))

# Define mesh
x = [  1; 20; 50 ];
y = [ 66; 15; -3 ];
# bearing angles (radians)
theta = [ 1.0; 0.74; 0.43 ];

# data vectors
c = cos( theta );
s = sin( theta );
# compose system matrix A
printf( "design matrix: A = \n" )
A = [ c, -s ]
printf( "data vector: b = \n" )
b = x .* c - y .* s

# solve least squares problem
printf( "least squares solution\n" )
printf( "xls = A \\ b:\n" )
xls = A \ b

# residual error vector
residual = A * xls - b;
printf( "residual error vector = A * xls - b\n" )

t2 = dot( residual, residual );
printf( "least total squared error t2 = residual . residual = %d\n", t2 )

# compute Gram matrix
W = transpose( A ) * A;

# invert Gram matrix
Winv = inv( W );
values = diag( Winv );

# measure design matrix
# m = rows, n = columns
[ m, n ] = size ( A );
g = sprintf('%d ', [ m, n ]);
fprintf('matrix dimensions: %s\n', g);

printf( "\ncompute error elements:\n" )
printf( "sigma = sqrt( t2 / ( m - n ) * values ):\n" )
sigma = sqrt( t2 / ( m - n ) * values )

printf( "\n#  #  #  Compare Octave values to exact values\n" )
printf( "\nFit parameters\n" )

printf( "\nerror in ground zero values\n" )
printf( "numericError = xls - Mathematica-xls\n" )
MathematicaXLS = [ 117.97723925949964161745199905235647691501049017468;
                   135.24677447077613795832279777569468400355063639720 ];
numericError = xls - MathematicaXLS

printf( "\nerror in ground zero values in machine epsilon\n" )
printf( "epsError = numericError ./ eps( 1.0 )\n" )
epsError = numericError ./ eps( 1.0 )

printf( "\nError parameters\n" )
printf( "\nground zero sigmas\n" )
printf( "numericError = sigma - sqrt( [ 108297055; 3419907 ] / 35 ) / 360\n" )
MathematicaSigma = [ 18.698052680295699237828157411268853967898756424020;
                     20.860166494699188800182633692615600495039424579191 ];
numericError = sigma - MathematicaSigma

printf( "\nerror in ground zero sigmas in machine epsilon\n" )
printf( "epsError = numericError ./ eps( 1.0 )\n" )
epsError = numericError ./ eps( 1.0 )

// dantopa@Quaxolotl.local:ground-zero $ octave-cli ground-zero.m
// Finding ground zero with bearing angles
// ans = 2023-01-16 12:39:41
// design matrix: A =
// A =
//
//    0.5403  -0.8415
//    0.7385  -0.6743
//    0.9090  -0.4169
//
// data vector: b =
// b =
//
//   -54.9968
//     4.6551
//    46.6989
//
// least squares solution
// xls = A \ b:
// xls =
//
//    117.98
//    135.25
//
// residual error vector = A * xls - b
// least total squared error t2 = residual . residual = 117.807
// matrix dimensions: 3 2
//
// compute error elements:
// sigma = sqrt( t2 / ( m - n ) * values ):
// sigma =
//
//    18.698
//    20.860
//
//
// #  #  #  Compare Octave values to exact values
//
// Fit parameters
//
// error in ground zero values
// numericError = xls - Mathematica-xls
// numericError =
//
//    1.4211e-14
//    5.6843e-14
//
//
// error in ground zero values in machine epsilon
// epsError = numericError ./ eps( 1.0 )
// epsError =
//
//     64
//    256
//
//
// Error parameters
//
// ground zero sigmas
// numericError = sigma - sqrt( [ 108297055; 3419907 ] / 35 ) / 360
// numericError =
//
//   -7.1054e-15
//   -7.1054e-15
//
//
// error in ground zero sigmas in machine epsilon
// epsError = numericError ./ eps( 1.0 )
// epsError =
//
//   -32
//   -32
