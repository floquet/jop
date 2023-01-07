#!/opt/local/bin/julia
# Solving ground zero triangulation with Julia
# https://stackoverflow.com/questions/22240581/running-julia-jl-files
println(" Running julia script '", PROGRAM_FILE, "'")
println( "Finding ground zero with bearing angle" )
using Dates
println( now( ) )

# Define mesh
x = [  1; 20; 50 ];
y = [ 66; 15; -3 ];
# bearing angles (radians)
theta = [ 1.0; 0.74; 0.43 ];

# data vectors
c = cos.( theta );
s = sin.( theta );
A = vcat( c, -s );
A = reshape( A, ( 3, 2 ) );

println( "")
println( "design matrix:")
println( "A = ", A )
println( "size( A ) = ", size( A ) )

xi  = x .* c
eta = y .* s
b   = xi - eta
println( "\ndata vector:")
println( "b = ", b )

xls = A \ b
println( "\nleast squares solution:")
println( "xls = ", xls )

# residual error vector
residual = A * xls - b
println( "" )
println( "residual error vector:" )
println( "residual = A * xls - b" )
println( "residual = ", residual )

# load linear algebra package
println( "" )
println( "using LinearAlgebra" )

# least total squared error
using LinearAlgebra
t2 = dot( residual, residual )
println( "" )
println( "t2 = ", t2 )

# compute Gram matrix
W = transpose( A ) * A
println( "" )
println( "compute Gram matrix:" )
println( "W = transpose( A ) * A" )
println( "W = ", W )

# invert Gram matrix
Winv = inv( W )
println( "" )
println( "invert Gram matrix:" )
println( "Winv = inv( W )" )
println( "Winv = ", Winv )

# harvest diagonal elements
values = diag( Winv )
println( "" )
println( "harvest diagonal elements of Winv:" )
println( "values = diag( Winv )" )
println( "values = ", values )

# rows and columns
( m, n ) =  size( A )
println( "")
println( "matrix dimensions ( rows, cols ):" )
println( "( m, n ) = ", ( m, n ) )

# compute error elements
sigma = sqrt.( t2 / ( m - n ) * values )
println( "" )
println( "compute error elements:" )
println( "sigma = sqrt( t2 / ( m - n ) * values )" )
println( "sigma = ", sigma )

println( "" )
println( "#  #  #  Compare Julia values to exact values" )

mathematicaX = 117.97723925949964161745199905235647691501049017468;
mathematicaY = 135.24677447077613795832279777569468400355063639720;
mathematicaSx = 18.698052680295699237828157411268853967898756424020;
mathematicaSy = 20.860166494699188800182633692615600495039424579191;

# compare julia to exact solution
#   solution values
numericError = xls - [ mathematicaX; mathematicaY ]
println( "" )
println( "error in intercept and slope values" )
println( "numericError = xls - [ mathematicaX; mathematicaY ]" )
println( "numericError = ", numericError )

epsError = numericError ./ eps( 1.0 )
println( "" )
println( "error in intercept and slope values in machine epsilon" )
println( "epsError = numericError ./ eps( 1.0 )" )
println( "epsError = ", epsError )

#   sigma values
numericError = sigma - [ mathematicaSx; mathematicaSy ]
println( "" )
println( "error in intercept and slope sigmas" )
println( "numericError = sigma - [ mathematicaSx; mathematicaSy ]" )
println( "numericError = ", numericError )

epsError = numericError ./ eps( 1.0 )
println( "" )
println( "error in intercept and slope sigmas in machine epsilon" )
println( "epsError = numericError ./ eps( 1.0 )" )
println( "epsError = ", epsError )

# dantopa@Xiuhcoatl.local:ground-zero $ julia ground_zero.jl
# Running julia script 'ground_zero.jl'
# Finding ground zero with bearing angle
# 2023-01-05T20:40:04.740

# design matrix:
# A = [0.5403023058681398 -0.8414709848078965; 0.7384685587295879 -0.674287911628145; 0.9089657496748851 -0.41687080242921076]
# size( A ) = (3, 2)

# data vector:
# b = [-54.99678269145303, 4.6550525001695835, 46.698899891031886]

# least squares solution:
# xls = [117.97723925949964, 135.24677447077616]

# residual error vector:
# residual = A * xls - b
# residual = [4.933920597302418, -8.727835773653505, 4.157938437457531]

# using LinearAlgebra

# t2 = 117.8071418020377

# compute Gram matrix:
# W = transpose( A ) * A
# W = [1.6634811280406097 -1.3315104171292993; -1.3315104171292993 1.3365188719593903]

# invert Gram matrix:
# Winv = inv( W )
# Winv = [2.9677078035099704 2.9565866507940366; 2.9565866507940366 3.693719578714401]

# harvest diagonal elements of Winv:
# values = diag( Winv )
# values = [2.9677078035099704, 3.693719578714401]

# matrix dimensions ( rows, cols ):
# ( m, n ) = (3, 2)

# compute error elements:
# sigma = sqrt( t2 / ( m - n ) * values )
# sigma = [18.698052680295692, 20.860166494699182]

# #  #  #  Compare Julia values to exact values

# error in intercept and slope values
# numericError = xls - [ mathematicaX; mathematicaY ]
# numericError = [0.0, 2.842170943040401e-14]

# error in intercept and slope values in machine epsilon
# epsError = numericError ./ eps( 1.0 )
# epsError = [0.0, 128.0]

# error in intercept and slope sigmas
# numericError = sigma - [ mathematicaSx; mathematicaSy ]
# numericError = [-7.105427357601002e-15, -7.105427357601002e-15]

# error in intercept and slope sigmas in machine epsilon
# epsError = numericError ./ eps( 1.0 )
# epsError = [-32.0, -32.0]
