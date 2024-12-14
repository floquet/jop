import re
from collections import defaultdict

def read_satellite_file(file_path):
    """
    Reads satellite data from a file, extracting every third line.

    Args:
        file_path (str): Path to the file.

    Returns:
        list: List of satellite data lines.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [line.strip() for i, line in enumerate(lines) if i % 3 == 0]

def group_satellites(data):
    """
    Groups satellites by their main category.

    Args:
        data (list): List of satellite names.

    Returns:
        dict: Dictionary with categories as keys and lists of satellites as values.
    """
    grouped = defaultdict(list)
    for satellite in data:
        match = re.match(r"([A-Z]+(?:\s?[A-Z]+)*)", satellite)
        if match:
            main_group = match.group(1)
            if "ASIASAT 8" in satellite and "AMOS-7" in satellite:
                main_group = "ASIASAT"
            grouped[main_group].append(satellite)
    return grouped

def generate_latex(grouped):
    """
    Generates LaTeX code for grouped satellite data.

    Args:
        grouped (dict): Grouped satellite data.

    Returns:
        str: LaTeX code.
    """
    latex_code = "\\begin{multicols}{2}\n\\begin{enumerate}\n"
    for category, satellites in sorted(grouped.items()):
        latex_code += f"  \\item {category}\n  \\begin{enumerate}[a.]\n"
        for satellite in sorted(satellites):
            latex_code += f"    \\item {satellite.replace('&', '\\&')}\n"
        latex_code += "  \\end{enumerate}\n"
    latex_code += "\\end{enumerate}\n\\end{multicols}\n"
    return latex_code

