#!/opt/local/bin/julia
# Including a shebang (#!/opt/local/bin/julia) at the top of your Julia script is necessary only if:
# 1. You intend to execute the script directly from the command line (e.g., ./script.jl) without explicitly calling `julia script.jl`.
# 	chmod +x mesh.jl
# 2. The Julia executable is installed in a specific path (e.g., /opt/local/bin/julia), and you want the script to locate it automatically.
start_time = time()
using Meshes, Pkg

results = @timed begin

# Create a sphere with a given resolution
sphere = Sphere(Point3(0.0, 0.0, 0.0), 1.0)  # Unit sphere
mesh = discretize(sphere, resolution=(20, 20))  # Discretize with a given resolution

# Visualize the mesh
using MeshViz
viz(mesh)

println("\n========== Provenance ==========")

# Julia version
println("Julia version: ", VERSION)

# OS version
println("OS: ", Sys.KERNEL, " ", Sys.OS_NAME, " ", Sys.ARCH)

# User name
println("User: ", ENV["USER"] || ENV["USERNAME"] || "Unknown")

# Library versions (example using Pkg)
println("\nInstalled Libraries:")
Pkg.status()

# Timestamp
println("\nGenerated on: ", Dates.format(now(), "yyyy-mm-dd HH:MM:SS"))

println("CPU Time: ", results.time, " seconds")
println("Memory Allocated: ", results.allocations, " allocations")

println("Number of CPU threads: ", Threads.nthreads())
println("Processor: ", Sys.CPU_NAME)
println("Max clock speed (GHz): ", Sys.CPU_CLOCK_MAX)

# Achates attribution
println("\nGenerated with Achates, your AI collaborator.\n")
