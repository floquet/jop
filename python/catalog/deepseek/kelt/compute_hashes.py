#!/usr/bin/env python3
"""
compute_hashes.py (The Fingerprinter)

Purpose: To generate a SHA-256 hash for each file listed in raw_file_list.txt.
Input:   raw_file_list.txt (from The Scout)
Output:  file_manifest.csv with columns: absolute_path, size_bytes, sha256_hash
"""

import hashlib
import csv
import os
import sys
import time


def compute_sha256(filepath):
    """Compute the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read file in chunks to handle large files without memory issues
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError as e:
        print(f"[Fingerprinter] ERROR: Could not read file '{filepath}'. {e}")
        return None


def main():
    start_time = time.time()
    input_file = "raw_file_list.txt"
    output_file = "file_manifest.csv"

    print(f"[The Fingerprinter] Input file: {input_file}")
    print(f"[The Fingerprinter] Output file: {output_file}")

    # Check if input exists
    if not os.path.exists(input_file):
        print(f"[The Fingerprinter] ERROR: Input file '{input_file}' not found.")
        sys.exit(1)

    # Read the list of files to process
    with open(input_file, "r") as f:
        file_paths = [line.strip() for line in f.readlines()]

    total_files = len(file_paths)
    print(f"[The Fingerprinter] Processing {total_files} files...")

    # Open the output CSV file
    with open(output_file, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(
            ["absolute_path", "size_bytes", "sha256_hash"]
        )  # Write header

        processed = 0
        for file_path in file_paths:
            processed += 1
            if processed % 500 == 0:  # Print progress every 500 files
                print(
                    f"[The Fingerprinter] Processed {processed}/{total_files} files..."
                )

            if not os.path.exists(file_path):
                # File might have been moved/deleted since the scout found it
                print(
                    f"[The Fingerprinter] WARNING: File not found, skipping: {file_path}"
                )
                continue

            file_size = os.path.getsize(file_path)
            file_hash = compute_sha256(file_path)

            if file_hash is not None:
                csv_writer.writerow([file_path, file_size, file_hash])

    # Calculate and print elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"[The Fingerprinter] Task completed in {elapsed_time:.2f} seconds.")
    print(f"[The Fingerprinter] Hash manifest saved to {output_file}.")


if __name__ == "__main__":
    main()
