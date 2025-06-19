#!/opt/local/bin/python3.9

import os
import sys
import platform
import datetime
from pathlib import Path
import nbformat as nbf


# === CORE BUILDERS ===
def new_markdown(text):
    return nbf.v4.new_markdown_cell(text)


def new_code(code):
    return nbf.v4.new_code_cell(code)


# === ORIGINAL COMPONENTS (UNTOUCHED) ===
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


def create_provenance_header():
    return new_markdown(
        "# Provenance Block\nThis notebook records system and environment details."
    )


def create_provenance_code():
    return new_code(
        """import os
import sys
import platform
import datetime
from pathlib import Path

# Get basic info
notebook_path = Path.cwd()
python_exec = sys.executable
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
user = os.getlogin()

# Print raw output
print("=== BASIC PROVENANCE ===")
print(f"Timestamp: {current_time}")
print(f"User: {user}")
print(f"Notebook location: {notebook_path}")

print("\\n=== SYSTEM ===")
print(f"OS: {platform.system()} {platform.release()}")
print(f"Machine: {platform.machine()}")
print(f"Processor: {platform.processor()}")

print("\\n=== PYTHON ===")
print(f"• Version: {platform.python_version()}")
print(f"• Executable: {sys.executable}")
print(f"• Implementation: {platform.python_implementation()}")"""
    )


def create_data_guide_markdown():
    return new_markdown(
        """# Satellite Data Acquisition Guide
## Step 1: Locate the Data Source
1. Visit the RBSP-ECT data portal:  
[https://rbsp-ect.newmexicoconsortium.org/rbsp_ect.php](https://rbsp-ect.newmexicoconsortium.org/rbsp_ect.php)

2. Click on **RBSP-A** spacecraft data:  
[Direct link](https://rbsp-ect.newmexicoconsortium.org/data_pub/rbspa/ECT/level2/)

## Step 2: Select Year
Choose 2018 data:  
[https://rbsp-ect.newmexicoconsortium.org/data_pub/rbspa/ECT/level2/2018/](https://rbsp-ect.newmexicoconsortium.org/data_pub/rbspa/ECT/level2/2018/)

## Step 3: Download Sample File
Download this sample CDF file (January 1, 2018):  
[rbspa_ect-elec-L2_20180101_v2.1.0.cdf](https://rbsp-ect.newmexicoconsortium.org/data_pub/rbspa/ECT/level2/2018/rbspa_ect-elec-L2_20180101_v2.1.0.cdf)

## Where to Save
Save the file in your notebook's data directory:  
`/path/to/your/notebook/data/`  
_(Use the exact path shown in your Provenance output)_

## Advanced: Download with wget

```bash
wget -P data/ https://rbsp-ect.newmexicoconsortium.org/data_pub/rbspa/ECT/level2/2018/rbspa_ect-elec-L2_20180101_v2.1.0.cdf
```"""
    )


def create_tag_markdown(tag):
    return new_markdown(f"# {tag}\n_Section begins here._")


def create_cdf_exploration_markdown():
    return new_markdown(
        """# CDF File Exploration Notebook
This notebook uses [`cdflib`](https://cdflib.readthedocs.io/) to explore NASA Common Data Format (.CDF) files.

## Features
- Lists all variables (`rVariables` and `zVariables`)
- Prints global and variable-specific attributes
- Shows data previews with shape and value summaries

## How It Works
We open the CDF using `cdflib.CDF(my_file)` and inspect its structure via `cdf_info()`, `globalattsget()`, 
`varinq()`, `varget()`, and `varattsget()`.
Each variable's shape and first few values are displayed. Variable attributes are printed. 
This helps you explore space weather data interactively and understand its layout before analysis."""
    )


def create_cdf_exploration_code():
    return new_code(
        """import cdflib
import numpy as np
from pathlib import Path
import urllib.request
import datetime

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# File information
file_url = "https://rbsp-ect.newmexicoconsortium.org/data_pub/rbspa/ECT/level2/2018/rbspa_ect-elec-L2_20180101_v2.1.0.cdf"
file_path = data_dir / "rbspa_ect-elec-L2_20180101_v2.1.0.cdf"
output_file = data_dir / "cdf_info.txt"

# Download the file if it doesn't exist
def download_file(url, destination):
    if not destination.exists():
        print(f"Downloading file from {url}...")
        urllib.request.urlretrieve(url, destination)
        print(f"File downloaded to {destination}")
    else:
        print(f"File already exists at {destination}")
    return destination

# Download the file
my_file = download_file(file_url, file_path)

# Open the CDF file
cdf_file = cdflib.CDF(my_file)
info = cdf_file.cdf_info()

# Open output file for writing
with open(output_file, 'w') as f:
    # Write file header
    f.write(f"CDF FILE ANALYSIS\\n")
    f.write(f"=================\\n")
    f.write(f"File: {file_path}\\n")
    f.write(f"Analysis date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
    
    # Write basic file information
    f.write("** CDF File Information **\\n")
    f.write(f"File path: {info.CDF}\\n")
    f.write(f"CDF Format Version: {info.Version}\\n")
    f.write(f"Encoding (Endianness): {info.Encoding}\\n")
    f.write(f"Majority (Storage Order): {info.Majority}\\n")

    if info.Num_rdim > 0:
        f.write(f"Number of rDimensions: {info.Num_rdim}\\n")
        f.write(f"rDimension sizes: {info.rDim_sizes}\\n")
    else:
        f.write("Number of rDimensions: 0\\n")

    rvars = info.rVariables
    zvars = info.zVariables
    f.write("\\n** Variables **\\n")
    f.write(f"rVariables: {rvars if rvars else 'None'}\\n")
    f.write(f"zVariables: {zvars if zvars else 'None'}\\n")

    global_attrs = cdf_file.globalattsget()
    f.write("\\n** Global Attributes **\\n")
    for attr, entries in global_attrs.items():
        if isinstance(entries, dict):
            f.write(f"- {attr}:\\n")
            for i, val in entries.items():
                f.write(f"    Entry {i}: {val}\\n")
        else:
            f.write(f"- {attr}: {entries}\\n")

    all_vars = list(rvars) + list(zvars)
    for var_name in all_vars:
        f.write(f"\\n** Variable: {var_name} **\\n")
        try:
            var_info = cdf_file.varinq(var_name)
            rec_vary = bool(var_info.Rec_Vary)
            dim_sizes = var_info.Dim_Sizes or []
            num_dims = var_info.Num_Dims
            if rec_vary:
                n_records = var_info.Last_Rec + 1
            else:
                n_records = 1
            if rec_vary and num_dims > 0:
                shape = (n_records, *dim_sizes)
            elif rec_vary:
                shape = (n_records,)
            else:
                shape = tuple(dim_sizes)
            f.write(f"Shape: {shape}\\n" if shape else "Shape: scalar\\n")

            if rec_vary:
                end_rec = min(var_info.Last_Rec, 4)
                data_preview = cdf_file.varget(var_name, startrec=0, endrec=end_rec)
            else:
                data_preview = cdf_file.varget(var_name)
        except Exception as e:
            data_preview = None
            f.write(f"Data: [Error reading: {e}]\\n")

        if data_preview is None:
            f.write("First values: None\\n")
        else:
            data_array = np.array(data_preview)
            snippet = data_array.flatten()[:5] if data_array.size > 10 else data_array
            f.write(f"Values: {snippet}\\n")

        var_attrs = cdf_file.varattsget(var_name)
        if var_attrs:
            f.write("Attributes:\\n")
            for attr, val in var_attrs.items():
                f.write(f"  - {attr}: {val}\\n")
        else:
            f.write("Attributes: (none)\\n")

print(f"CDF file information written to {output_file}")

# Return the CDF file object for further exploration
cdf_file"""
    )


# === NOTEBOOK ASSEMBLY ===
def create_master_notebook():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        create_provenance_header(),
        create_provenance_code(),
        create_data_guide_markdown(),
        create_tag_markdown("=== CDF EXPLORATION ==="),
        create_cdf_exploration_markdown(),
        create_cdf_exploration_code(),
        create_tag_markdown("=== BASIC PLOTS ==="),
        create_tag_markdown("=== ORBITAL MECHANICS ==="),
    ]
    return nb


# === EXECUTION ===
if __name__ == "__main__":
    print_provenance()
    notebook = create_master_notebook()
    Path("master-space-weather-analysis.ipynb").write_text(nbf.writes(notebook))
    print("jupyter notebook master-space-weather-analysis.ipynb")
