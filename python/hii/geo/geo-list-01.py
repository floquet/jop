import os
import sys
import datetime
import uuid
import re
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Generate a unique run ID
run_id = uuid.uuid4()

# Collect runtime metadata
def get_runtime_metadata():
    metadata = {
        "Run ID": str(run_id),
        "HOSTNAME": os.environ.get("HOSTNAME", "Unknown"),
        "Working Directory": os.getcwd(),
        "Script": os.path.basename(__file__) if "__file__" in globals() else "Interactive Session",
        "Python Version": sys.version,
        "Timestamp": str(datetime.datetime.now()),
    }
    return metadata

# Log metadata to a file
def log_metadata(metadata, log_file_path="script_log.txt"):
    with open(log_file_path, "a") as log_file:
        log_file.write("\n===== Runtime Metadata =====\n")
        for key, value in metadata.items():
            log_file.write(f"{key}: {value}\n")
        log_file.write("=" * 40 + "\n")

# Display runtime metadata
def display_metadata(metadata):
    print("\n===== Runtime Metadata =====")
    for key, value in metadata.items():
        print(f"{key}: {value}")
    print("=" * 40)

# Function to read and process the file
def read_satellite_file(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        # Take every 3rd line starting from the 1st
        satellite_data = [line.strip() for i, line in enumerate(lines) if i % 3 == 0]
        return satellite_data
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        sys.exit(1)

# Function to group satellites
def group_satellites(data):
    grouped = defaultdict(list)
    for satellite in data:
        # Extract the main category (e.g., ASIASAT, AMOS)
        match = re.match(r"([A-Z]+(?:\s?[A-Z]+)*)", satellite)
        if match:
            main_group = match.group(1)
            # Handle specific edge cases like ASIASAT 8 (AMOS-7)
            if "ASIASAT 8" in satellite and "AMOS-7" in satellite:
                main_group = "ASIASAT"
            grouped[main_group].append(satellite)
    return grouped

# Function to generate LaTeX
def generate_latex(grouped):
    latex_code = "\\begin{multicols}{2}\n"  # Use two columns for better formatting
    latex_code += "\\begin{enumerate}\n"
    for category, satellites in sorted(grouped.items()):
        latex_code += f"  \\item {category}\n"
        latex_code += "  \\begin{enumerate}[a.]\n"
        for satellite in sorted(satellites):
            # Escape special characters for LaTeX
            satellite = satellite.replace("&", "\\&")
            latex_code += f"    \\item {satellite}\n"
        latex_code += "  \\end{enumerate}\n"
    latex_code += "\\end{enumerate}\n"
    latex_code += "\\end{multicols}\n"
    return latex_code

# Main function
def main():
    # Update the path to your file here
    file_path = "geo.txt"  # Replace with your actual file path
    satellite_data = read_satellite_file(file_path)
    
    # Group and process the data
    grouped_satellites = group_satellites(satellite_data)
    
    # Generate LaTeX output
    latex_output = generate_latex(grouped_satellites)
    
    # Save the LaTeX output to a file
    output_file = "satellites.tex"
    with open(output_file, "w") as file:
        file.write(latex_output)
    
    logging.info(f"LaTeX output written to {output_file}")
    
    # Display and log runtime metadata
    metadata = get_runtime_metadata()
    display_metadata(metadata)
    log_metadata(metadata)

if __name__ == "__main__":
    main()
