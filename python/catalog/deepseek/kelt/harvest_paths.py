#!/usr/bin/env python3
"""
harvest_paths.py (The Scout)

Purpose: To traverse a defined set of directories and locate every .nb file.
Input:   List of root paths (passed as command-line arguments).
Output:  A file 'raw_file_list.txt' containing the absolute path of every .nb file found.
Tool:    The Unix `find` command.
"""

import sys
import subprocess
import os
import time


def main(search_paths):
    """
    The main function of The Scout.
    Executes the `find` command for each given path and collates the results.
    """
    start_time = time.time()  # Start the timer
    output_filename = "raw_file_list.txt"

    print(f"[The Scout] Target file patterns: *.nb")
    print(f"[The Scout] Search paths: {search_paths}")
    print(f"[The Scout] Output file: {output_filename}")

    # Check if the output file exists and warn if we are going to overwrite it
    if os.path.exists(output_filename):
        print(
            f"[The Scout] WARNING: {output_filename} already exists. It will be overwritten."
        )
        # Simple safety check
        response = input("[The Scout] Continue? (y/N): ").strip().lower()
        if response != "y":
            print("[The Scout] Aborted by user.")
            sys.exit(0)

    all_found_files = []  # List to hold all found paths

    # Loop through each provided search path
    for a_path in search_paths:
        # Basic check: does the path exist?
        if not os.path.exists(a_path):
            print(f"[The Scout] WARNING: Path '{a_path}' does not exist. Skipping.")
            continue

        print(f"[The Scout] Searching: {a_path}")

        # Build the find command
        # find [path] -name "*.nb" -type f
        # KEY FIX: Add '-xdev' to stay on one filesystem and ignore mount points like /Volumes/ if they are dead.
        # Alternatively, use more robust options:
        cmd = ["find", "-L", a_path, "-name", "*.nb", "-type", "f"]
        # The '-L' option tells find to follow symbolic links.
        # ECHO THE COMMAND (Your request)
        print(f"[The Scout] Command: {' '.join(cmd)}")

        try:
            # Run the command, capture the output
            # KEY FIX: Use `text=True` to get a string instead of bytes, and don't use `check=True`.
            # We'll check the return code manually to be more graceful.
            result = subprocess.run(cmd, capture_output=True, text=True)

            # Check if find had any errors
            if result.returncode != 0:
                print(
                    f"[The Scout] WARNING: 'find' had errors (code {result.returncode}), but may have found files."
                )
                print(
                    f"[The Scout] stderr: {result.stderr[:500]}..."
                )  # Print first 500 chars of error

            # Process the output regardless of the error code
            files_from_this_path = result.stdout.splitlines()
            all_found_files.extend(files_from_this_path)
            print(f"[The Scout] Found {len(files_from_this_path)} files in this path.")

        except Exception as e:
            # Catch any other unexpected errors
            print(
                f"[The Scout] ERROR: Failed to run 'find' on path '{a_path}'. Error: {e}"
            )
            # Let's continue with other paths

    # Write all found paths to the output file
    print(
        f"[The Scout] Writing {len(all_found_files)} total paths to {output_filename}..."
    )
    try:
        with open(output_filename, "w") as f:
            for file_path in all_found_files:
                f.write(file_path + "\n")
        print(f"[The Scout] Successfully wrote {output_filename}.")
    except IOError as e:
        print(
            f"[The Scout] FATAL ERROR: Could not write to {output_filename}. Error: {e}"
        )
        sys.exit(1)

    # Calculate and print elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"[The Scout] Task completed in {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    # The command-line arguments passed to this script are the paths to search.
    paths_to_search = sys.argv[1:]

    if not paths_to_search:
        print("[The Scout] ERROR: No search paths provided.")
        print("Usage: python harvest_paths.py [path1] [path2] ...")
        sys.exit(1)

    main(paths_to_search)
