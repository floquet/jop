#!/opt/local/bin/julia
# Including a shebang (#!/opt/local/bin/julia) at the top of your Julia script is necessary only if:
# 1. You intend to execute the script directly from the command line (e.g., ./script.jl) without explicitly calling `julia script.jl`.
# 2. The Julia executable is installed in a specific path (e.g., /opt/local/bin/julia), and you want the script to locate it automatically.

start_time = time()
using Plots

# Parameters for discretization
n_lat = 20  # Number of latitude lines
n_lon = 40  # Number of longitude lines

# Generate points on the sphere
points = [(sin(θ) * cos(φ), sin(θ) * sin(φ), cos(θ))
    for θ in range(0, π, length=n_lat)
    for φ in range(0, 2π, length=n_lon)]

# Scatter plot to visualize
scatter([p[1] for p in points], [p[2] for p in points], [p[3] for p in points], legend=false)
