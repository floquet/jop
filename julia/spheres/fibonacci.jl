using Plots

function fibonacci_sphere(n::Int)
    points = Vector{Tuple{Float64, Float64, Float64}}()
    phi = (1 + √5) / 2  # Golden ratio
    for i in 0:n-1
        z = 1 - (2 * i) / (n - 1)
        radius = √(1 - z^2)
        theta = 2π * i / phi
        push!(points, (radius * cos(theta), radius * sin(theta), z))
    end
    return points
end

# Generate and visualize
points = fibonacci_sphere(1000)
scatter([p[1] for p in points], [p[2] for p in points], [p[3] for p in points], legend=false)

println("\n========== Provenance ==========")

# Julia version
println("Julia version: ", VERSION)

# OS version
println("OS: ", Sys.KERNEL, " ", Sys.OS_NAME, " ", Sys.ARCH)

# User name
println("User: ", ENV["USER"] || ENV["USERNAME"] || "Unknown")

# Library versions (example using Pkg)
using Pkg
println("\nInstalled Libraries:")
Pkg.status()

# Timestamp
println("\nGenerated on: ", Dates.format(now(), "yyyy-mm-dd HH:MM:SS"))

# Achates attribution
println("\nGenerated with Achates, your AI collaborator.\n")
