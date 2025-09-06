#!/usr/bin/env python3
"""
create_mathematica_library.py

Master script to orchestrate the deduplication and curation of Mathematica .nb files.
Orchestrates the component scripts: The Scout, The Fingerprinter, The Brain, The Librarian, The Cartographer.

Usage: python create_mathematica_library.py

kelt: AS-5 "Kelt" (Kh-11/KSR-2) NATO designation
"""

import datetime
import os
import pwd
import platform
import sys
import subprocess

# --- Configuration Section: USER EDITS HERE --- #
# Define the root directories to search for .nb files
SEARCH_PATHS = ["/Volumes/mathematica/", "/Users/dantopa/"]
# Define where the final canonical library should be built
LIBRARY_ROOT = "/Users/dantopa/Mathematica_Library"
# Define the name of the final output database
OUTPUT_DATABASE = "./mathematica_library.db"
# Define the trailhead patterns for parsing project context
TRAILHEAD_PATTERNS = "_nb,.nb,nb/"

# --- Component Script Names --- #
SCRIPT_HARVEST = "harvest_paths.py"
SCRIPT_HASHES = "compute_hashes.py"
SCRIPT_ANALYZE = "parse_and_analyze.py"
SCRIPT_BUILD = "build_library.py"
SCRIPT_DATABASE = "generate_database.py"


# --- Provenance Function --- #
def print_provenance():
    """Print system and environment information for provenance and debugging."""
    print("\n" + "=" * 60)
    print("PROVENANCE & EXECUTION CONTEXT")
    print("=" * 60)
    print("Timestamp:   ", datetime.datetime.now())
    print("Source:       %s/%s" % (os.getcwd(), os.path.basename(__file__)))
    try:
        print("User ID:      ", pwd.getpwuid(os.getuid()).pw_name)
    except Exception:
        print("User ID:      ", "Could not retrieve username")
    print("Platform:     ", platform.platform())
    # Print Python version info in a cleaner way
    print("Python:       %s" % sys.version.split(" (")[0])
    print("Interpreter:  %s" % sys.executable)
    print("Working Dir:  %s" % os.getcwd())
    print("Scripts Dir:  Contents of current directory:")
    for f in os.listdir("."):
        if f.endswith(".py"):
            print("             ", f)
    print("=" * 60 + "\n")


# --- Main Orchestration Function --- #
def main():
    """Orchestrate the entire workflow by calling component scripts in sequence."""

    # Print provenance information at the start of the run
    print_provenance()

    print("### THE DIGITAL LIBRARIAN: MASTER SCRIPT ###")
    print("### PHASE 1: Harvesting Paths (The Scout) ###")
    # Build command: python3 harvest_paths.py [path1] [path2] ...
    cmd_harvest = [sys.executable, SCRIPT_HARVEST] + SEARCH_PATHS
    print(f"Running: {' '.join(cmd_harvest)}")
    try:
        subprocess.run(cmd_harvest, check=True)
        print("✓ Harvesting completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"✗ Harvesting failed with error code {e.returncode}.")
        sys.exit(1)  # Exit the master script if a component fails

    print("### PHASE 2: Computing Hashes (The Fingerprinter) ###")
    cmd_hashes = [sys.executable, SCRIPT_HASHES]
    print(f"Running: {' '.join(cmd_hashes)}")
    try:
        subprocess.run(cmd_hashes, check=True)
        print("✓ Hash computation completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"✗ Hash computation failed with error code {e.returncode}.")
        sys.exit(1)

    print("### PHASE 3: Parsing and Analyzing (The Brain) ###")
    # Pass the trailhead patterns as an argument
    cmd_analyze = [sys.executable, SCRIPT_ANALYZE, "--trailheads", TRAILHEAD_PATTERNS]
    print(f"Running: {' '.join(cmd_analyze)}")
    try:
        subprocess.run(cmd_analyze, check=True)
        print("✓ Analysis completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"✗ Analysis failed with error code {e.returncode}.")
        sys.exit(1)

    print("### PHASE 4: Building Library (The Librarian) ###")
    cmd_build = [sys.executable, SCRIPT_BUILD, "--library", LIBRARY_ROOT]
    print(f"Running: {' '.join(cmd_build)}")
    try:
        subprocess.run(cmd_build, check=True)
        print("✓ Library construction completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"✗ Library construction failed with error code {e.returncode}.")
        sys.exit(1)

    print("### PHASE 5: Generating Final Database (The Cartographer) ###")
    cmd_database = [sys.executable, SCRIPT_DATABASE, "--output", OUTPUT_DATABASE]
    print(f"Running: {' '.join(cmd_database)}")
    try:
        subprocess.run(cmd_database, check=True)
        print("✓ Final database generation completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"✗ Final database generation failed with error code {e.returncode}.")
        sys.exit(1)

    # Final success message
    print("🎉" * 10)
    print("LIBRARY CREATION COMPLETE!")
    print(f"Canonical Library: {LIBRARY_ROOT}")
    print(f"Query Database:    {os.path.abspath(OUTPUT_DATABASE)}")
    print("🎉" * 10)


# Standard boilerplate to call the main() function.
if __name__ == "__main__":
    main()
