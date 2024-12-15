#!/opt/local/bin/julia
# shebang ( #!/opt/local/bin/julia ) necessary only:
# 1. to execute the script directly from the command line ( e.g., ./*.jl ) without explicitly calling `julia *.jl`.
#   chmod +x mesh.jl
#   chmod u+x script.sh : only the file owner to execute the script
#   chmod 700 script.sh : read, write, and execute
# 2. or if Julia executable is installed in a specific path ( e.g., /opt/local/bin/julia ), and you want the script to locate it automatically.

# provenance.jl: Install required packages for the project
using Pkg, Dates, CpuId

start_time = time(  )

# Start timer
start_time = time(  )

# Provenance block
function define_os(  )
    kernel_string = string( Sys.KERNEL )  # Convert Symbol to String
    if occursin( "Microsoft", kernel_string )
        return "Windows"
    elseif occursin( "Darwin", kernel_string )
        return "macOS"
    elseif occursin( "Linux", kernel_string )
        return "Linux"
    else
        return "Unknown"
    end
end

os_name = define_os(  )

# Absolute path of the script
script_path = Base.abspath(  @__FILE__  )


println( "\n========== Provenance ==========" )
println( "Script Path: ", script_path )
println( "Julia version: ", VERSION )
println( "OS: ", Sys.KERNEL, " ", os_name, " ", Sys.ARCH )
println( "User: ", get( ENV, "USER", get( ENV, "USERNAME", "Unknown" ) ) )
println( "Number of CPU threads: ", Threads.nthreads(  ) )
println( "Processor: ", CpuId.cpubrand(  ) )  # Detailed CPU brand
println( "CPU Base Frequency ( GHz ): ", CpuId.cpu_base_frequency(  ) / 1e9 )
println( "CPU Max Frequency ( GHz ): ", CpuId.cpu_max_frequency(  ) / 1e9 )

println( "\nInstalled Libraries:" )
Pkg.status(  )

# End timer
end_time = time(  )

# Timestamp
println( "\nGenerated on: ", Dates.format( now(  ), "yyyy-mm-dd HH:MM:SS" ) )
println( "Execution time: ", round( end_time - start_time, digits=2 ), " seconds" )

# Achates attribution
println( "\nGenerated with Achates, your AI collaborator.\n" )

# dantopa@Xiuhcoatl:util $ ./provenance.jl 

# ========== Provenance ==========
# Script Path: /Users/dantopa/repos-xiuhcoatl/github/jop/julia/util/provenance.jl
# Julia version: 1.11.2
# OS: Darwin macOS x86_64
# User: dantopa
# Number of CPU threads: 1
# Processor: Intel(R) Core(TM) i7-8700B CPU @ 3.20GHz
# CPU Base Frequency ( GHz ): 3.2e-6
# CPU Max Frequency ( GHz ): 4.6e-6

# Installed Libraries:
# Status `~/.julia/environments/v1.11/Project.toml`
#   [adafc99b] CpuId v0.3.1
#   [9ecf9c4f] MeshViz v0.8.8
# ⌅ [eacbb407] Meshes v0.32.3
#   [91a5bcdd] Plots v1.40.9
# Info Packages marked with ⌅ have new versions available but compatibility constraints restrict them from upgrading. To see why use `status --outdated`

# Generated on: 2024-12-14 20:05:30
# Execution time: 1.37 seconds

# Generated with Achates, your AI collaborator.
