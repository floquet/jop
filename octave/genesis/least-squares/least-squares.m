A = [ 1 1; 1 2; 1 3; 1 4; 1 5; 1 6; 1 7; 1 8; 1 9 ];
println( "")
println( "design matrix:")
println( "A = ", A )

# rows and columns
( m, n ) =  size( A )
println( "")
println( "matrix dimensions ( rows, cols ):" )
println( "( m, n ) = ", ( m, n ) )

# Define data
T = [ 78/5; 35/2; 183/5; 219/5; 291/5; 308/5; 321/5; 352/5; 494/5 ];
println( "")
println( "data vector:" )
println( "T = ", T )

# least squares solution
xls = A \ T
println( "")
println( "least squares solution vector:" )
println( "xls = A \\ T" )
println( "xls = ", xls )
