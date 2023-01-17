# Ground zero from bearing angles
# https:#octave.discourse.group/t/error-sourcing-file-octaverc/2417
#   indicates error in file

printf( "Finding ground zero with bearing angles\n" )
disp( strftime ("%Y-%m-%d %H:%M:%S", localtime (time ())) )

# Define mesh
x = [  1; 20; 50 ];
y = [ 66; 15; -3 ];
# bearing angles (radians)
theta = [ 1.0; 0.74; 0.43 ];

# data vectors
c = cos( theta );
s = sin( theta );

# form linear system Ax = b
A = [ c, -s ];
b = x .* c - y .* s;

# inner products
cc = dot(c, c);
cs = dot(c, s);
ss = dot(s, s);
cb = dot(c, b);
sb = dot(s, b);

det  = cc * ss - cs^2;

# normal equations solution
Winv = [ ss cs; cs cc] / det;
atb  = [ cb; -sb ];

# least squares solution: xls
xls  = Winv * atb;

# residual error vector
residual = A * xls - b;

t2 = dot( residual, residual );
values = diag( Winv );

# measure linear system
# m = rows (measurements), n = columns (free variables)
m = length ( b );
n = length ( xls );
g = sprintf('%d ', [ m, n ]);

sigma = sqrt( t2 / ( m - n ) * values );
MathematicaXLS = [ 117.97723925949964161745199905235647691501049017468;
                   135.24677447077613795832279777569468400355063639720 ];
numericError = xls - MathematicaXLS;
gzError = numericError ./ eps( 1.0 );

MathematicaSigma = [ 18.698052680295699237828157411268853967898756424020;
                     20.860166494699188800182633692615600495039424579191 ];
numericError = sigma - MathematicaSigma;
sigmaError = numericError ./ eps( 1.0 );

# https:#www.mathworks.com/help/matlab/ref/fprintf.html
printf ( "particular least squares solution for ground zero\n" )
printf( "x0 = %4.15f +/- %4.15f\n", xls( 1 ), sigma( 1 ) )
printf( "y0 = %4.15f +/- %4.15f\n", xls( 2 ), sigma( 2 ) )

printf( "\nErrors in machine epsilon = %d\n", eps( 1.0 ) )
printf( "x0 = %d +/- %d\n", gzError( 1 ), sigmaError( 1 ) )
printf( "y0 = %d +/- %d\n", gzError( 2 ), sigmaError( 2 ) )

# dantopa@Quaxolotl.local:ground-zero $ octave-cli strict-ground-zero.m 
# Finding ground zero with bearing angles
# 2023-01-16 14:46:27
# particular least squares solution for ground zero
# x0 = 117.977239259499584 +/- 18.698052680295692
# y0 = 135.246774470776103 +/- 20.860166494699182
#
# Errors in machine epsilon = 2.22045e-16
# x0 = -256 +/- -32
# y0 = -128 +/- -32
