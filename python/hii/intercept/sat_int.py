import numpy as np  # For vector operations and mathematical calculations
import datetime  # For recording execution time
import os  # For filesystem operations
import pwd  # For retrieving user ID information
import platform  # For system and platform details
import sys  # For Python version information
import matplotlib.pyplot as plt  # For plotting trajectories
from matplotlib.animation import FuncAnimation  # For creating animations

def pr_provenance():
    """Print system provenance."""
    print("\nExecution Provenance")
    print("=" * 40)
    print("\n", datetime.datetime.now())
    print("Source:  %s/%s" % (os.getcwd(), os.path.basename(__file__)))
    print("User ID:", pwd.getpwuid(os.getuid()).pw_name)
    print("Platform Info:")
    print("    Platform: ", platform.platform())
    print("    Uname:    ", platform.uname())
    print("Version Info:")
    print("    Python:   %s" % sys.version)
    print("    Numpy:   ", np.__version__)
    print("=" * 40)

def plot_trajectories(prey_path, predator_path):
    """Plot the trajectories of the prey and predator."""
    prey_path = np.array(prey_path)
    predator_path = np.array(predator_path)

    plt.figure(figsize=(8, 8))
    plt.plot(prey_path[:, 0], prey_path[:, 1], label="Prey Trajectory", linestyle='--')
    plt.plot(predator_path[:, 0], predator_path[:, 1], label="Predator Trajectory")
    plt.scatter(prey_path[-1, 0], prey_path[-1, 1], color='blue', label="Prey's Final Position")
    plt.scatter(predator_path[-1, 0], predator_path[-1, 1], color='red', label="Predator's Final Position")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.title("Predator-Prey Interception Trajectories")
    plt.legend()
    plt.grid()
    plt.show()

def animate_trajectories(prey_path, predator_path):
    """Create an animation of the trajectories."""
    prey_path = np.array(prey_path)
    predator_path = np.array(predator_path)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_title("Predator-Prey Interception Animation")
    ax.set_xlabel("X Position (m)")
    ax.set_ylabel("Y Position (m)")

    prey_line, = ax.plot([], [], 'b--', label="Prey Trajectory")
    predator_line, = ax.plot([], [], 'r-', label="Predator Trajectory")
    prey_point, = ax.plot([], [], 'bo', label="Prey")
    predator_point, = ax.plot([], [], 'ro', label="Predator")
    ax.legend()

    def update(frame):
        prey_line.set_data(prey_path[:frame, 0], prey_path[:frame, 1])
        predator_line.set_data(predator_path[:frame, 0], predator_path[:frame, 1])
        prey_point.set_data(prey_path[frame, 0], prey_path[frame, 1])
        predator_point.set_data(predator_path[frame, 0], predator_path[frame, 1])
        return prey_line, predator_line, prey_point, predator_point

    anim = FuncAnimation(fig, update, frames=len(prey_path), interval=50, blit=True)
    plt.show()

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
    prey_loc     = np.array( [ 0.0, 0.0, 0.0 ] )  # Start at origin
    predator_loc = np.array( [ 15.0, 15.0, 0.0 ] )  # Start at a distant point
    prey_vel     = np.array( [ 1.0, 0.0, 0.0 ] )  # Prey moves in +x direction
    predator_vel = np.array( [ 0.0, 0.0, 0.0 ] )  # Predator initially stationary

    # Simulation variables
    t0 = 0.0
    k = 0
    detected = False
    prey_path = [ prey_loc.copy() ]
    predator_path = [ predator_loc.copy() ]

    def norm2( vec ):
        """Compute the Euclidean norm of a vector."""
        return np.linalg.norm( vec )

    # Open output file
    with open( "simulation_output.txt", "w" ) as file_out:
        print( "Starting simulation..." )

        while True:
            t = t0 + k * delta_t

            # --- Write current state to file ---
            file_out.write( f"{t} {prey_loc.tolist()} {predator_loc.tolist()} {prey_vel.tolist()} {predator_vel.tolist()}" )

            # --- Update Prey's Position ---
            prey_loc = prey_loc + prey_vel * delta_t

            # --- Compute Distance Between Prey and Predator ---
            d_prey_predator = norm2( predator_loc - prey_loc )

            # --- Detection Phase ---
            if not detected:
                # Compute detection probability ( increases as d_prey_predator decreases )
                p_detect = p_max * np.exp( -d_prey_predator / R_d )
                if np.random.random() < p_detect:
                    detected = True
                    print( f"Prey detected at time t = {t:.2f} s" )

            # --- Interception Phase ---
            if detected:
                # Compute unit vector direction, predator to prey
                direction = ( prey_loc - predator_loc ) / norm2( prey_loc - predator_loc )

                # Update predator's velocity and position
                predator_vel = direction * v_predator
                predator_loc = predator_loc + predator_vel * delta_t

                # Check if predator intercepts prey
                if d_prey_predator < epsilon:
                    print( f"Predator intercepted prey at time t = {t:.2f} s" )
                    print( f"Final position of prey: {prey_loc}" )
                    print( f"Final position of predator: {predator_loc}" )
                    break

            # Record paths
            prey_path.append( prey_loc.copy() )
            predator_path.append( predator_loc.copy() )

            # --- Update Simulation Time ---
            k += 1

    # Plot trajectories
    print("Plotting the trajectories of the prey and predator...")
    print("Inputs:")
    print(" - prey_path: List of prey's positions over time.")
    print(" - predator_path: List of predator's positions over time.")
    print("Output:")
    print(" - A static plot showing the paths of the prey and predator, with their initial and final positions highlighted.")
    plot_trajectories(prey_path, predator_path)

    # Animate trajectories
    print("Animating the trajectories of the prey and predator...")
    print("Inputs:")
    print(" - prey_path: List of prey's positions over time.")
    print(" - predator_path: List of predator's positions over time.")
    print("Output:")
    print(" - An animation showing the motion of the prey and predator as they move over time.")
    animate_trajectories(prey_path, predator_path)