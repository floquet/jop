#!/opt/local/bin/julia
using Pkg
using Dates
using CpuId  # Use CpuId for detailed CPU information

# Start timer
start_time = time()

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
println("Processor: ", CpuId.cpubrand())  # Detailed CPU brand
println("CPU Vendor: ", CpuId.cpuvendor())  # CPU vendor name
println("CPU Base Frequency (GHz): ", CpuId.cpu_base_frequency() / 1e9)
println("CPU Max Frequency (GHz): ", CpuId.cpu_max_frequency() / 1e9)

println("\nInstalled Libraries:")
Pkg.status()

# End timer
end_time = time()

# Timestamp
println("\nGenerated on: ", Dates.format(now(), "yyyy-mm-dd HH:MM:SS"))
println("Execution time: ", round(end_time - start_time, digits=2), " seconds")

# Achates attribution
println("\nGenerated with Achates, your AI collaborator.\n")