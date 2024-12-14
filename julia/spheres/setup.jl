#!/opt/local/bin/julia
# Including a shebang (#!/opt/local/bin/julia) at the top of your Julia script is necessary only if:
# 1. You intend to execute the script directly from the command line (e.g., ./script.jl) without explicitly calling `julia script.jl`.
# 2. The Julia executable is installed in a specific path (e.g., /opt/local/bin/julia), and you want the script to locate it automatically.

# setup.jl: Install required packages for the project
start_time = time()

using Pkg

# List of required packages
packages = [
    "Meshes",
    "MeshViz",
    "Plots",
    # Add more packages here
]

# Install missing packages
for pkg in packages
    if !haskey(Pkg.dependencies(), pkg)
        println("Installing ", pkg)
        Pkg.add(pkg)
    else
        println(pkg, " is already installed.")
    end
end

println("All packages installed!")

end_time = time()

println("\n========== Provenance ==========")
println("Julia version: ", VERSION)
println("OS: ", Sys.KERNEL, " ", Sys.OS_NAME, " ", Sys.ARCH)
println("User: ", ENV["USER"] || ENV["USERNAME"] || "Unknown")
println("\nCPU Time Used: ", round(end_time - start_time, digits=3), " seconds")
println("Number of CPU threads: ", Threads.nthreads())
println("Processor: ", Sys.CPU_NAME)
println("Max clock speed (GHz): ", Sys.CPU_CLOCK_MAX)

# Library versions
println("\nInstalled Libraries:")
Pkg.status()

# Timestamp
using Dates
println("\nGenerated on: ", Dates.format(now(), "yyyy-mm-dd HH:MM:SS"))

# Achates attribution
println("\nGenerated with Achates, your AI collaborator.\n")
