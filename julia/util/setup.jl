#!/opt/local/bin/julia
# Including a shebang (#!/opt/local/bin/julia) at the top of your Julia script is necessary only if:
# 1. You intend to execute the script directly from the command line (e.g., ./script.jl) without explicitly calling `julia script.jl`.
# 2. The Julia executable is installed in a specific path (e.g., /opt/local/bin/julia), and you want the script to locate it automatically.

# setup.jl: Install required packages for the project
start_time = time()

# This script relies on Julia's package manager (Pkg), which operates independently of MacPorts.
# It is cross-platform as long as the required system libraries for the packages are available.
using Pkg

# List of required packages
packages = [
    "Meshes",
    "MeshViz",
    "Plots",
    # Add more packages here
]

# Install missing packages
# Consider running this script after installing or updating Julia, or when managing dependencies for a specific project.
# This ensures all required packages are present and updated.
for pkg in packages
    if !haskey(Pkg.dependencies(), Symbol(pkg))  # Fixed: `Symbol(pkg)` for correct comparison
        println("Installing ", pkg)
        Pkg.add(pkg)
    else
        println(pkg, " is already installed.")
    end
end

# You might note that this script is particularly useful when sharing projects or setting up a new environment to ensure all dependencies are installed.
println("All packages installed!")

end_time = time()

println("\n========== Provenance ==========")

# Detect OS
define_os() = begin
    kernel_string = String(Sys.KERNEL)  # Convert Sys.KERNEL to a String
    if occursin("Microsoft", kernel_string)
        "Windows"
    elseif occursin("Darwin", kernel_string)
        "macOS"
    elseif occursin("Linux", kernel_string)
        "Linux"
    else
        "Unknown"
    end
end

os_name = define_os()

# Provenance block
println("Julia version: ", VERSION)
println("OS: ", Sys.KERNEL, " ", os_name, " ", Sys.ARCH)
println("User: ", ENV["USER"] || ENV["USERNAME"] || "Unknown")
println("User: ", get(ENV, "USER", get(ENV, "USERNAME", "Unknown")))
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