import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib import animation

# =============================================================================
# Physics Setup
# =============================================================================
# Constants
mu = 3.986004418e14  # Earth's gravitational parameter (m^3/s^2)
R = 6771000.0        # Radius of initial circular orbit (m) ~ 400 km altitude
m = 1.0              # Mass of object (kg) - irrelevant for trajectory

# Initial orbital period and angular rate
T_circ = 2 * np.pi * np.sqrt(R**3 / mu)
omega = 2 * np.pi / T_circ

# Perturbation size
delta = 100.0  # 100 meter perturbation

# Time parameters (integrate for 1.5 orbits)
t_span = (0, 1.5 * T_circ)
t_eval = np.linspace(0, 1.5 * T_circ, 1000)

# =============================================================================
# Initial Conditions Calculation
# =============================================================================
# 1. Initial circular orbit state at theta=0 (on x-axis)
r0_circ = np.array([R, 0.0])
v0_circ = np.array([0.0, np.sqrt(mu / R)])

# 2. Pure Radial Perturbation: Just move the position radially
r0_radial = r0_circ * (1 + delta/R)  # Position: R + delta
v0_radial = v0_circ.copy()           # Velocity: unchanged

print("Pure Radial Perturbation:")
print(f"  Position: [{r0_radial[0]:.1f}, {r0_radial[1]:.1f}] m")
print(f"  Velocity: [{v0_radial[0]:.3f}, {v0_radial[1]:.3f}] m/s")
print(f"  Predicted apoapsis: {R + 3*delta:.1f} m")

# 3. CW-style Perturbation: Move position AND add prograde burn
r0_cw = r0_radial.copy()  # Same position: R + delta

# Calculate the required delta-v (from our derivation)
dv_mag = (3 * np.sqrt(mu/R) * delta) / (2 * R)
v0_cw = v0_circ + np.array([0.0, dv_mag])  # Add prograde burn

print("\nCW-style Perturbation (with burn):")
print(f"  Position: [{r0_cw[0]:.1f}, {r0_cw[1]:.1f}] m")
print(f"  Velocity: [{v0_cw[0]:.3f}, {v0_cw[1]:.3f}] m/s")
print(f"  Delta-v applied: {dv_mag:.6f} m/s")
print(f"  Predicted apoapsis: {R + 7*delta:.1f} m")

# =============================================================================
# Equations of Motion - 2D Kepler Problem
# =============================================================================
def kepler_equations(t, state):
    """Equations of motion for 2D Kepler problem"""
    x, y, vx, vy = state
    r = np.sqrt(x**2 + y**2)
    r3 = r**3
    
    # Derivatives: [dx/dt, dy/dt, dvx/dt, dvy/dt]
    dxdt = vx
    dydt = vy
    dvxdt = -mu * x / r3
    dvydt = -mu * y / r3
    
    return [dxdt, dydt, dvxdt, dvydt]

# =============================================================================
# Numerical Integration
# =============================================================================
# Initial state vectors: [x, y, vx, vy]
initial_state_circ = [r0_circ[0], r0_circ[1], v0_circ[0], v0_circ[1]]
initial_state_radial = [r0_radial[0], r0_radial[1], v0_radial[0], v0_radial[1]]
initial_state_cw = [r0_cw[0], r0_cw[1], v0_cw[0], v0_cw[1]]

# Solve the ODEs for all three cases
print("\nIntegrating trajectories...")
sol_circ = solve_ivp(kepler_equations, t_span, initial_state_circ, t_eval=t_eval, rtol=1e-8)
sol_radial = solve_ivp(kepler_equations, t_span, initial_state_radial, t_eval=t_eval, rtol=1e-8)
sol_cw = solve_ivp(kepler_equations, t_span, initial_state_cw, t_eval=t_eval, rtol=1e-8)

# Extract positions
x_circ, y_circ = sol_circ.y[0], sol_circ.y[1]
x_radial, y_radial = sol_radial.y[0], sol_radial.y[1]
x_cw, y_cw = sol_cw.y[0], sol_cw.y[1]

# Calculate distances from Earth
r_circ = np.sqrt(x_circ**2 + y_circ**2)
r_radial = np.sqrt(x_radial**2 + y_radial**2)
r_cw = np.sqrt(x_cw**2 + y_cw**2)

# =============================================================================
# Plotting
# =============================================================================
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Orbits in 2D space
earth = plt.Circle((0, 0), R, color='blue', alpha=0.3, label='Earth')
ax1.add_patch(earth)
ax1.plot(x_circ, y_circ, 'w-', alpha=0.5, label='Reference Circular Orbit')
ax1.plot(x_radial, y_radial, 'cyan', label=f'Radial Perturbation (Δ={delta}m)')
ax1.plot(x_cw, y_cw, 'magenta', label=f'CW-style (Δv={dv_mag:.4f} m/s)')

# Mark initial points
ax1.plot(r0_radial[0], r0_radial[1], 'o', color='cyan', markersize=8, label='Perturbation Start')
ax1.plot(r0_cw[0], r0_cw[1], 'o', color='magenta', markersize=8)

ax1.set_xlabel('X Position (m)')
ax1.set_ylabel('Y Position (m)')
ax1.set_title('Orbital Trajectories')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.axis('equal')

# Plot 2: Radial distance over time
time_hours = t_eval / 3600  # Convert seconds to hours
ax2.plot(time_hours, r_circ/R, 'w-', alpha=0.5, label='Reference Orbit')
ax2.plot(time_hours, r_radial/R, 'cyan', label='Radial Perturbation')
ax2.plot(time_hours, r_cw/R, 'magenta', label='CW-style Perturbation')

# Mark predicted extremes
ax2.axhline(y=(R + 3*delta)/R, color='cyan', linestyle='--', alpha=0.7, label='Predicted $R+3\Delta$')
ax2.axhline(y=(R + 7*delta)/R, color='magenta', linestyle='--', alpha=0.7, label='Predicted $R+7\Delta$')
ax2.axhline(y=1.0, color='white', linestyle=':', alpha=0.5)

ax2.set_xlabel('Time (hours)')
ax2.set_ylabel('Radial Distance (R)')
ax2.set_title('Radial Oscillation: Theory vs Simulation')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('orbital_perturbation_comparison.png', dpi=150, bbox_inches='tight')
plt.show()

# =============================================================================
# Print final results and validation
# =============================================================================
print(f"\n=== RESULTS ===")
print(f"Reference circular orbit radius: {R/1000:.1f} km")
print(f"Perturbation size Δ: {delta} m")
print(f"Reference orbital period: {T_circ/60:.1f} minutes")

print(f"\nRadial perturbation case:")
print(f"  Max radius: {np.max(r_radial)-R:.1f} m above R (Predicted: {3*delta:.1f} m)")
print(f"  Min radius: {R-np.min(r_radial):.1f} m below R")

print(f"\nCW-style perturbation case:")
print(f"  Max radius: {np.max(r_cw)-R:.1f} m above R (Predicted: {7*delta:.1f} m)")
print(f"  Min radius: {R-np.min(r_cw):.1f} m below R")
print(f"  Energy ratio (CW/Radial): {np.max(r_cw)/np.max(r_radial):.2f}")

# =============================================================================
# Energy Analysis (Optional)
# =============================================================================
def orbital_energy(x, y, vx, vy):
    """Calculate specific orbital energy"""
    r = np.sqrt(x**2 + y**2)
    v_sq = vx**2 + vy**2
    return v_sq/2 - mu/r

# Calculate energies
E_circ = orbital_energy(x_circ, y_circ, sol_circ.y[2], sol_circ.y[3])
E_radial = orbital_energy(x_radial, y_radial, sol_radial.y[2], sol_radial.y[3])
E_cw = orbital_energy(x_cw, y_cw, sol_cw.y[2], sol_cw.y[3])

print(f"\n=== ENERGY ANALYSIS ===")
print(f"Circular orbit energy: {np.mean(E_circ):.6e} m²/s²")
print(f"Radial perturbation energy: {np.mean(E_radial):.6e} m²/s²")
print(f"CW-style energy: {np.mean(E_cw):.6e} m²/s²")
print(f"Energy ratio (CW/Radial): {np.mean(E_cw)/np.mean(E_radial):.2f}")