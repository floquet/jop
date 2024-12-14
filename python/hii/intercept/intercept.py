import numpy as np

def pr_provenance():
    """Print system provenance."""
    print("\nExecution Provenance")
    print("=" * 40)
    print("\n", datetime.datetime.now())
    print("source:  %s/%s" % (os.getcwd(), os.path.basename(__file__)))
    print("user id:", pwd.getpwuid(os.getuid()).pw_name)
    print("platform info:")
    print("    platform: ", platform.platform())
    print("    uname:    ", platform.uname())
    print("version info:")
    print("    python:   %s" % sys.version)
    print("    numpy:   ", np.__version__)
    #print("    pandas:  ", pd.__version__)
    #print("    matplotlib: ", plt.matplotlib.__version__)
    print("=" * 40)

# Main execution
if __name__ == "__main__":
# Parameters
delta_t = 0.1  # Time step (s)
epsilon = 0.01  # Interception tolerance (m)
v_predator = 1.0  # Speed of predator (m/s)
prey_max_vel = 2.0  # Maximum speed of prey (m/s)
R_d = 10.0  # Maximum detection range (m)
p_max = 0.9  # Maximum detection probability

# Initialize positions and velocities
prey_loc = np.array([0.0, 0.0, 0.0])  # Start at origin
predator_loc = np.array([15.0, 15.0, 0.0])  # Start at a distant point
prey_vel = np.array([1.0, 0.0, 0.0])  # Prey moves in +x direction
predator_vel = np.array([0.0, 0.0, 0.0])  # Predator initially stationary

# Simulation variables
t = 0.0
detected = False

# Helper functions
def norm2(vec):
    """Compute the Euclidean norm of a vector."""
    return np.linalg.norm(vec)

# Open output file
with open("simulation_output.txt", "w") as file_out:
    print("Starting simulation...")

    while True:
        # --- Write current state to file ---
        file_out.write(f"{t} {prey_loc.tolist()} {predator_loc.tolist()} {prey_vel.tolist()} {predator_vel.tolist()}\n")

        # --- Update Prey's Position ---
        prey_loc = prey_loc + prey_vel * delta_t

        # --- Compute Distance Between Prey and Predator ---
        d_prey_predator = norm2(predator_loc - prey_loc)

        # --- Detection Phase ---
        if not detected:
            # Compute detection probability (increases as d_prey_predator decreases)
            p_detect = p_max * np.exp(-d_prey_predator / R_d)
            if np.random.random() < p_detect:
                detected = True
                print(f"Prey detected at time t = {t:.2f} s")

        # --- Interception Phase ---
        if detected:
            # Compute unit vector direction, predator to prey
            direction = (prey_loc - predator_loc) / norm2(prey_loc - predator_loc)

            # Update predator's velocity and position
            predator_vel = direction * v_predator
            predator_loc = predator_loc + predator_vel * delta_t

            # Check if predator intercepts prey
            if d_prey_predator < epsilon:
                print(f"Predator intercepted prey at time t = {t:.2f} s")
                print(f"Final position of prey: {prey_loc}")
                print(f"Final position of predator: {predator_loc}")
                break

        # --- Update Simulation Time ---
        t += delta_t