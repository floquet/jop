#! /opt/local/bin/python3.9

import os
import sys
import platform
import datetime
from pathlib import Path
import nbformat as nbf


# === PROVENANCE PRINTER ===
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


# === NOTEBOOK CELL BUILDERS ===


def create_provenance_header():
    return nbf.v4.new_markdown_cell(
        "# Provenance Block\nThis notebook records system and environment details."
    )


def create_provenance_code():
    return nbf.v4.new_code_cell(
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
print(f"• Implementation: {platform.python_implementation()}")
"""
    )


def create_data_guide_markdown():
    return nbf.v4.new_markdown_cell(
        "# Satellite Data Acquisition Guide\n"
        "## Step 1: Locate the Data Source\n"
        "1. Visit the RBSP-ECT data portal:  \n"
        "[https://rbsp-ect.newmexicoconsortium.org/rbsp_ect.php](https://rbsp-ect.newmexicoconsortium.org/rbsp_ect.php)\n\n"
        "2. Click on **RBSP-A** spacecraft data:  \n"
        "[Direct link](https://rbsp-ect.newmexicoconsortium.org/data_pub/rbspa/ECT/level2/)\n\n"
        "## Step 2: Select Year\n"
        "Choose 2018 data:  \n"
        "[https://rbsp-ect.newmexicoconsortium.org/data_pub/rbspa/ECT/level2/2018/](https://rbsp-ect.newmexicoconsortium.org/data_pub/rbspa/ECT/level2/2018/)\n\n"
        "## Step 3: Download Sample File\n"
        "Download this sample CDF file (January 1, 2018):  \n"
        "[rbspa_ect-elec-L2_20180101_v2.1.0.cdf](https://rbsp-ect.newmexicoconsortium.org/data_pub/rbspa/ECT/level2/2018/rbspa_ect-elec-L2_20180101_v2.1.0.cdf)\n\n"
        "## Where to Save\n"
        "Save the file in your notebook's data directory:  \n"
        "`/path/to/your/notebook/data/`  \n"
        "_(Use the exact path shown in your Provenance output)_\n\n"
        "## Advanced: Download with wget\n\n"
        "```bash\n"
        "wget -P data/ https://rbsp-ect.newmexicoconsortium.org/data_pub/rbspa/ECT/level2/2018/rbspa_ect-elec-L2_20180101_v2.1.0.cdf\n"
        "```"
    )


def create_tag_markdown(tag):
    return nbf.v4.new_markdown_cell(f"# {tag}\n_Section begins here._")


def create_cdf_exploration_markdown():
    return nbf.v4.new_markdown_cell(
        "# CDF File Exploration Notebook\n"
        "This notebook uses [`cdflib`](https://cdflib.readthedocs.io/) to explore NASA Common Data Format (.CDF) files.\n\n"
        "## Features\n"
        "- Lists all variables (`rVariables` and `zVariables`)\n"
        "- Prints global and variable-specific attributes\n"
        "- Shows data previews with shape and value summaries\n\n"
        "## How It Works\n"
        "We open the CDF using `cdflib.CDF(my_file)` and inspect its structure via `cdf_info()`, `globalattsget()`, "
        "`varinq()`, `varget()`, and `varattsget()`.\n"
        "Each variable's shape and first few values are displayed. Variable attributes are printed. "
        "This helps you explore space weather data interactively and understand its layout before analysis."
    )


def create_cdf_exploration_code():
    return nbf.v4.new_code_cell(
        """import cdflib
import numpy as np

cdf_file = cdflib.CDF(my_file)
info = cdf_file.cdf_info()

print("** CDF File Information **")
print(f"File path: {info.CDF}")
print(f"CDF Format Version: {info.Version}")
print(f"Encoding (Endianness): {info.Encoding}")
print(f"Majority (Storage Order): {info.Majority}")

if info.Num_rdim > 0:
    print(f"Number of rDimensions: {info.Num_rdim}")
    print(f"rDimension sizes: {info.rDim_sizes}")
else:
    print("Number of rDimensions: 0")

rvars = info.rVariables
zvars = info.zVariables
print("\\n** Variables **")
print(f"rVariables: {rvars if rvars else 'None'}")
print(f"zVariables: {zvars if zvars else 'None'}")

global_attrs = cdf_file.globalattsget()
print("\\n** Global Attributes **")
for attr, entries in global_attrs.items():
    if isinstance(entries, dict):
        print(f"- {attr}:")
        for i, val in entries.items():
            print(f"    Entry {i}: {val}")
    else:
        print(f"- {attr}: {entries}")

all_vars = list(rvars) + list(zvars)
for var_name in all_vars:
    print(f"\\n** Variable: {var_name} **")
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
        print(f"Shape: {shape}" if shape else "Shape: scalar")

        if rec_vary:
            end_rec = min(var_info.Last_Rec, 4)
            data_preview = cdf_file.varget(var_name, startrec=0, endrec=end_rec)
        else:
            data_preview = cdf_file.varget(var_name)
    except Exception as e:
        data_preview = None
        print(f"Data: [Error reading: {e}]")

    if data_preview is None:
        print("First values: None")
    else:
        data_array = np.array(data_preview)
        snippet = data_array.flatten()[:5] if data_array.size > 10 else data_array
        print(f"Values: {snippet}")

    var_attrs = cdf_file.varattsget(var_name)
    if var_attrs:
        print("Attributes:")
        for attr, val in var_attrs.items():
            print(f"  - {attr}: {val}")
    else:
        print("Attributes: (none)")
"""
    )


# === CREATE: master-space-weather-analysis.ipynb ===
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

    path_out = Path("master-space-weather-analysis.ipynb")
    with path_out.open("w") as f:
        nbf.write(nb, f)

    print(f"\nCreated: {path_out}")
    print(f"To run:  jupyter notebook {path_out}")


# === ENTRY POINT ===
if __name__ == "__main__":
    print_provenance()
    create_master_notebook()
