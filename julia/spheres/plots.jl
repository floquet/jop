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
