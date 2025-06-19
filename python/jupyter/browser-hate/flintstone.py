#!/usr/bin/env python

import os
import sys
import platform
import datetime
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
import cdflib
from datetime import timedelta


# Print basic provenance information
def print_provenance():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = os.getlogin()
    notebook_path = Path.cwd()

    print("\n=== BASIC PROVENANCE ===")
    print(f"Timestamp: {current_time}")
    print(f"User: {user}")
    print(f"Notebook location: {notebook_path}")

    print("\n=== SYSTEM ===")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")

    print("\n=== PYTHON ===")
    print(f"• Version: {platform.python_version()}")
    print(f"• Executable: {sys.executable}")
    print(f"• Implementation: {platform.python_implementation()}")


# Main function
def main():
    print_provenance()

    # File path
    file_path = Path("data/rbspa_ect-elec-L2_20180101_v2.1.0.cdf")
    print(f"Using existing file: {file_path}")

    # Open the CDF file
    cdf_file = cdflib.CDF(file_path)

    # Get time data
    epoch_data = cdf_file.varget("Epoch")
    times = cdflib.cdfepoch.encode(epoch_data)

    # Get position data
    pos_data = None
    vel_data = None

    # Try to find position and velocity variables
    variables = cdf_file.cdf_info().zVariables

    # Look for position and velocity variables
    for var in variables:
        var_attrs = cdf_file.varattsget(var)
        if "FIELDNAM" in var_attrs:
            field_name = var_attrs["FIELDNAM"]
            if "POSITION" in field_name.upper():
                pos_data = cdf_file.varget(var)
                print(f"Found position data in variable: {var}")
            elif "VELOCITY" in field_name.upper():
                vel_data = cdf_file.varget(var)
                print(f"Found velocity data in variable: {var}")

    # If not found by field name, try common variable names
    if pos_data is None:
        for pos_var in ["SC_POS", "POS", "POSITION", "R"]:
            if pos_var in variables:
                pos_data = cdf_file.varget(pos_var)
                print(f"Found position data in variable: {pos_var}")
                break

    if vel_data is None:
        for vel_var in ["SC_VEL", "VEL", "VELOCITY", "V"]:
            if vel_var in variables:
                vel_data = cdf_file.varget(vel_var)
                print(f"Found velocity data in variable: {vel_var}")
                break

    # If still not found, list all variables and exit
    if pos_data is None or vel_data is None:
        print("Could not find position or velocity data. Available variables:")
        for var in variables:
            var_attrs = cdf_file.varattsget(var)
            if "FIELDNAM" in var_attrs:
                print(f"- {var}: {var_attrs['FIELDNAM']}")
            else:
                print(f"- {var}")
        return

    # Calculate radius (magnitude of position vector)
    radius = np.sqrt(pos_data[:, 0] ** 2 + pos_data[:, 1] ** 2 + pos_data[:, 2] ** 2)

    # Calculate velocity magnitude
    velocity = np.sqrt(vel_data[:, 0] ** 2 + vel_data[:, 1] ** 2 + vel_data[:, 2] ** 2)

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot radius
    ax1.plot(times, radius)
    ax1.set_title("Spacecraft Radius vs Time")
    ax1.set_ylabel("Radius (km)")
    ax1.set_xlabel("Time (UTC)")
    ax1.grid(True)

    # Plot velocity
    ax2.plot(times, velocity)
    ax2.set_title("Spacecraft Velocity vs Time")
    ax2.set_ylabel("Velocity (km/s)")
    ax2.set_xlabel("Time (UTC)")
    ax2.grid(True)

    # Adjust layout and save
    plt.tight_layout()
    plt.savefig("spacecraft_orbit.png")
    print("Plot saved as spacecraft_orbit.png")

    # Show plot
    plt.show()


if __name__ == "__main__":
    main()
