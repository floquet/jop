#!/opt/local/bin/julia
# Solving ground zero triangulation with Julia
# https://stackoverflow.com/questions/22240581/running-julia-jl-files
println(" Running julia script '", PROGRAM_FILE, "'")
using Dates
println( now( ) )
println( "Finding ground zero with bearing angles" )

# define mesh
x = [  1; 20; 50 ]
y = [ 66; 15; -3 ]
# bearing angles (radians)
theta = [ 1.0; 0.74; 0.43 ]

# data vectors
c = cos.( theta )
s = sin.( theta )

# construct linear system
A = [ c'; -s' ]'
b  = x .* c - y .* s

# load linear algebra package for dot product
using LinearAlgebra
cc = dot(c, c)
cs = dot(c, s)
ss = dot(s, s)
cb = dot(c, b)
sb = dot(s, b)

det  = cc * ss - cs^2

# normal equations solution
Winv = [ ss cs; cs cc] / det
atb  = [ cb; -sb ]
xls  = Winv * atb

# error propagation
residual = A * xls - b
t2 = dot( residual, residual )
values = diag( Winv )
# m = rows (measurements), n = columns (free variables)
( m, n ) =  size( A )
# compute error elements
sigma = sqrt.( t2 / ( m - n ) * values )

println( "" )
println( "particular least squares solution for ground zero" )
println( "xls = $xls" )
println( "      +/- $sigma" )

mathematicaX  = 117.97723925949964161745199905235647691501049017468;
mathematicaY  = 135.24677447077613795832279777569468400355063639720;
mathematicaSx = 18.698052680295699237828157411268853967898756424020;
mathematicaSy = 20.860166494699188800182633692615600495039424579191;

# compare julia to exact solution
#   solution values
xlsError   = xls - [ mathematicaX; mathematicaY ]
epsXLSrror = xlsError ./ eps( 1.0 )

#   sigma values
sigmaError    = sigma - [ mathematicaSx; mathematicaSy ]
epsSigmaError = sigmaError ./ eps( 1.0 )

println( "" )
println( "error in intercept and slope in machine epsilon sigmas" )
println( "xls = $epsXLSrror +/- $epsSigmaError\n" )

# dantopa@Quaxolotl.local:ground-zero $ julia ground_zero_breve.jl 
#  Running julia script 'ground_zero_breve.jl'
# 2023-01-27T20:34:53.153
# Finding ground zero with bearing angles
#
# particular least squares solution for ground zero
# xls = [117.97723925949958, 135.2467744707761]
#       +/- [18.698052680295692, 20.860166494699182]
#
# error in intercept and slope in machine epsilon sigmas
# xls = [-256.0, -128.0] +/- [-32.0, -32.0]
