#!/usr/bin/env python3
"""
create_mathematica_library.py

Master script to orchestrate the deduplication and curation of Mathematica .nb files.
Orchestrates the component scripts: The Scout, The Fingerprinter, The Brain, The Librarian, The Cartographer.

Usage: python create_mathematica_library.py
"""

import datetime
import os
import pwd
import platform
import sys
import subprocess

# --- Configuration Section: USER EDITS HERE --- #
# SEARCH_PATHS = [
#    "/Users/dantopa/Dropbox/_mm"  # The real location of your Mathematica_files
# ]
SEARCH_PATHS = ["/Volumes/mathematica/", "/Users/dantopa/"]
LIBRARY_ROOT = "/Users/dantopa/Mathematica_Library"
OUTPUT_DATABASE = "./mathematica_library.db"
TRAILHEAD_PATTERNS = "_nb,.nb,nb/"

# --- Component Script Names and Their OUTPUT Files --- #
# This defines what file each script produces.
# This is key for checking if a phase has already been completed.
PHASES = {
    "harvest": {
        "script": "harvest_paths.py",
        "output": "raw_file_list.txt",
        "desc": "Harvesting Paths (The Scout)",
    },
    "hash": {
        "script": "compute_hashes.py",
        "output": "file_manifest.csv",
        "desc": "Computing Hashes (The Fingerprinter)",
    },
    "analyze": {
        "script": "parse_and_analyze.py",
        "output": "analysis.db",  # Or whatever your brain script outputs
        "desc": "Parsing and Analyzing (The Brain)",
    },
    "build": {
        "script": "build_library.py",
        "output": LIBRARY_ROOT,  # This one is a directory
        "desc": "Building Library (The Librarian)",
    },
    "database": {
        "script": "generate_database.py",
        "output": OUTPUT_DATABASE,
        "desc": "Generating Final Database (The Cartographer)",
    },
}


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
    print("Python:       %s" % sys.version.split(" (")[0])
    print("Interpreter:  %s" % sys.executable)
    print("Working Dir:  %s" % os.getcwd())
    print("=" * 60 + "\n")


def ask_to_skip(phase_name, output_target):
    """Ask the user what to do if a phase's output already exists."""
    print(f"\n*** PHASE: {phase_name} ***")
    print(f"Output target '{output_target}' already exists.")
    print("Options:")
    print("  (s)kip - Use the existing output and move to the next phase.")
    print("  (o)verwrite - Delete the old output and re-run this phase.")
    print("  (a)bort - Stop the entire process.")

    while True:
        response = input("Choose (s/o/a): ").strip().lower()
        if response in ("s", "skip"):
            return "skip"
        elif response in ("o", "overwrite"):
            # For safety, confirm overwrite
            confirm = (
                input(f"Confirm OVERWRITE of '{output_target}'? (y/N): ")
                .strip()
                .lower()
            )
            if confirm == "y":
                # Try to remove the existing output
                try:
                    if os.path.isfile(output_target):
                        os.remove(output_target)
                    elif os.path.isdir(output_target):
                        import shutil

                        shutil.rmtree(output_target)
                    print(f"Removed {output_target}.")
                except OSError as e:
                    print(f"Error removing {output_target}: {e}")
                    return "abort"
                return "overwrite"
            else:
                print("Overwrite cancelled.")
                return "ask_again"
        elif response in ("a", "abort"):
            return "abort"
        else:
            print("Please choose 's', 'o', or 'a'.")


# --- Main Orchestration Function --- #
def main():
    """Orchestrate the entire workflow by calling component scripts in sequence."""
    print_provenance()
    print("### THE DIGITAL LIBRARIAN: MASTER SCRIPT ###")

    # Define the order of execution
    execution_order = ["harvest", "hash", "analyze", "build", "database"]

    for phase_key in execution_order:
        phase_info = PHASES[phase_key]
        output_target = phase_info["output"]

        # Check if the output of this phase already exists
        output_exists = os.path.exists(output_target)

        if output_exists:
            action = ask_to_skip(phase_info["desc"], output_target)
            if action == "skip":
                print(f"✓ Skipping phase: {phase_info['desc']}")
                continue
            elif action == "abort":
                print("Process aborted by user.")
                sys.exit(0)
            # If 'overwrite', we just continue to run the phase normally

        # Run the phase
        print(f"### {phase_info['desc']} ###")

        if phase_key == "harvest":
            cmd = [sys.executable, phase_info["script"]] + SEARCH_PATHS
        elif phase_key == "analyze":
            cmd = [
                sys.executable,
                phase_info["script"],
                "--trailheads",
                TRAILHEAD_PATTERNS,
            ]
        elif phase_key == "build":
            cmd = [sys.executable, phase_info["script"], "--library", LIBRARY_ROOT]
        elif phase_key == "database":
            cmd = [sys.executable, phase_info["script"], "--output", OUTPUT_DATABASE]
        else:  # 'hash' and any other simple phases
            cmd = [sys.executable, phase_info["script"]]

        print(f"Running: {' '.join(cmd)}")
        try:
            subprocess.run(cmd, check=True)
            print(f"✓ {phase_info['desc']} completed successfully.\n")
        except subprocess.CalledProcessError as e:
            print(f"✗ {phase_info['desc']} failed with error code {e.returncode}.")
            sys.exit(1)

    # Final success message
    print("🎉" * 10)
    print("LIBRARY CREATION COMPLETE!")
    print(f"Canonical Library: {LIBRARY_ROOT}")
    print(f"Query Database:    {os.path.abspath(OUTPUT_DATABASE)}")
    print("🎉" * 10)


if __name__ == "__main__":
    main()
