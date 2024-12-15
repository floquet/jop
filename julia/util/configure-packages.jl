#!/opt/local/bin/julia
# shebang (#!/opt/local/bin/julia) necessary only:
# 1. to execute the script directly from the command line (e.g., ./*.jl) without explicitly calling `julia *.jl`.
#   chmod +x mesh.jl
#   chmod u+x script.sh : only the file owner to execute the script
#   chmod 700 script.sh : read, write, and execute
# 2. or if Julia executable is installed in a specific path (e.g., /opt/local/bin/julia), and you want the script to locate it automatically.

# configure-packages.jl: Install required packages for the project
start_time = time()

# This script relies on Julia's package manager (Pkg), which operates independently of MacPorts.
# It is cross-platform as long as the required system libraries for the packages are available.
using Pkg, Dates

# List of required packages
packages = [
    "Meshes",
    "MeshViz",
    "Plots",
    "Sysinfo"
    # Add more packages here
]

end_time = time()

# Timestamp
println( "\nGenerated on: ", Dates.format( now( ), "yyyy-mm-dd HH:MM:SS" ) )
println( "Execution time: ", round( end_time - start_time, digits=  2 ), " seconds" )
