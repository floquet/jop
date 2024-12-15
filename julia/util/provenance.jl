#!/opt/local/bin/julia
# shebang (#!/opt/local/bin/julia) necessary only:
# 1. to execute the script directly from the command line (e.g., ./*.jl) without explicitly calling `julia *.jl`.
#   chmod +x mesh.jl
#   chmod u+x script.sh : only the file owner to execute the script
#   chmod 700 script.sh : read, write, and execute
# 2. or if Julia executable is installed in a specific path (e.g., /opt/local/bin/julia), and you want the script to locate it automatically.

# provenance.jl: Install required packages for the project
start_time = time()
using Pkg
using Dates
using Sysinfo  # Add Sysinfo for system details

# Provenance block
function define_os()
    kernel_string = string(Sys.KERNEL)  # Convert Symbol to String
    if occursin("Microsoft", kernel_string)
        return "Windows"
    elseif occursin("Darwin", kernel_string)
        return "macOS"
    elseif occursin("Linux", kernel_string)
        return "Linux"
    else
        return "Unknown"
    end
end

os_name = define_os()

println("\n========== Provenance ==========")
println("Julia version: ", VERSION)
println("OS: ", Sys.KERNEL, " ", os_name, " ", Sys.ARCH)
println("User: ", get(ENV, "USER", get(ENV, "USERNAME", "Unknown")))
println("Number of CPU threads: ", Threads.nthreads())
println("Processor: ", Sys.CPU_NAME)
println("Max clock speed (GHz): ", Sysinfo.cpu_max_freq() / 1e3)  # Use Sysinfo to get max CPU frequency

println("\nInstalled Libraries:")
Pkg.status()

end_time = time()

# Timestamp
println("\nGenerated on: ", Dates.format(now(), "yyyy-mm-dd HH:MM:SS"))
println("Execution time: ", round(end_time - start_time, digits=2), " seconds")

# Achates attribution
println("\nGenerated with Achates, your AI collaborator.\n")