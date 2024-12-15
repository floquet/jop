#!/opt/local/bin/julia
# shebang (  #!/opt/local/bin/julia  ) necessary only:
# 1. to execute the script directly from the command line (  e.g., ./*.jl  ) without explicitly calling `julia *.jl`.
#   chmod +x mesh.jl
#   chmod u+x script.sh : only the file owner to execute the script
#   chmod 700 script.sh : read, write, and execute
# 2. or if Julia executable is installed in a specific path (  e.g., /opt/local/bin/julia  ), and you want the script to locate it automatically.

# configure-packages.jl: Install required packages for the project
using LinearAlgebra

# Input data
X = 1:9  # Measurements
b = [ 78/5, 35/2, 183/5, 219/5, 291/5, 308/5, 321/5, 352/5, 494/5 ]  # Data vector

# Design matrix A
A = hcat(  ones(  length(  X  )  ), X  )

# Solve for x using the normal equations A' * A * x = A' * b
W = A' * A         # Weight matrix
Delta = det(  W  )     # Determinant of W
alpha = inv(  W  )     # Curvature matrix
x = W \ (  A' * b  )   # Least-squares solution

# Residuals and sum of squares of residuals
residual = A * x - b
r2 = sum(  residual.^2  )

# Singular values and condition number
sigma = svdvals(  A  )
kappa = maximum(  sigma  ) / minimum(  sigma  )

# Errors (  uncertainties in parameters  )
uncertainties = sqrt.(  diag(  alpha  )  )

# Reference values from Mathematica
mathematica_solution = [ 1733 / 360, 1129 / 120 ]  # Intercept, Slope
mathematica_uncertainties = [ sqrt( 21659411 / 7 ) / 360, sqrt( 1139969 / 105 ) / 120 ]
mathematica_r2 = 1139969 / 3600
mathematica_sigma = [ sqrt( 3 * ( 49 + sqrt( 2341 ) ) ), sqrt( 3 * ( 49 - sqrt( 2341 ) ) ) ]
mathematica_kappa = sqrt( ( 49 + sqrt( 2341 ) ) / ( 49 - sqrt( 2341 ) ) )

# Compute differences in terms of machine epsilon
function compare_with_epsilon( computed, reference, label )
    diff = abs( computed - reference )
    epsilon_diff = diff / eps( computed )
    println( "$label: $( round( epsilon_diff, digits=2 ) ) eps ( $( round( diff, sigdigits=3 ) ) )" )
end

# Output prominently the Julia results
println( "\n==============================" )
println( " Julia Results ( Normal Equations + LinearAlgebra )" )
println( "==============================" )
println( "Intercept ( c₀ ): ", x[ 1 ] )
println( "Slope ( c₁ ): ", x[ 2 ] )
println( "Residual sum of squares ( r² ): ", r2 )
println( "Singular values ( σ ): ", sigma )
println( "Matrix condition number ( κ ): ", kappa )
println( "Uncertainties ( ε ): ", uncertainties )
println( "==============================" )

# Comparison with Mathematica results
println( "\n==============================" )
println( " Differences from Mathematica ( in Machine Epsilon )" )
println( "==============================" )
compare_with_epsilon( x[ 1 ], mathematica_solution[ 1 ], "Intercept ( c₀ )" )
compare_with_epsilon( x[ 2 ], mathematica_solution[ 2 ], "Slope ( c₁ )" )
compare_with_epsilon( r2, mathematica_r2, "Residual sum of squares ( r² )" )
compare_with_epsilon( uncertainties[ 1 ], mathematica_uncertainties[ 1 ], "Uncertainty in c₀" )
compare_with_epsilon( uncertainties[ 2 ], mathematica_uncertainties[ 2 ], "Uncertainty in c₁" )
compare_with_epsilon( sigma[ 1 ], mathematica_sigma[ 1 ], "Singular value σ₁" )
compare_with_epsilon( sigma[ 2 ], mathematica_sigma[ 2 ], "Singular value σ₂" )
compare_with_epsilon( kappa, mathematica_kappa, "Condition number ( κ )" )
println( "==============================" )
