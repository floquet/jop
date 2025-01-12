#!/usr/bin/env python3
"""
WorldCat Bibliography Enhancer

Description:
    This script processes a `.bib` file, extracts ISBNs, fetches WorldCat IDs,
    and appends the WorldCat ID to the entries. It includes minimal provenance
    for troubleshooting module dependencies related to WorldCat functionality.

Author: Daniel
Date: January 10, 2025
"""

import os
import sys
import datetime
import requests
import re

def pr_provenance():
    """Print minimal provenance for WorldCat functionality."""
    print("\nExecution Provenance")
    print("=" * 40)
    print("\n", datetime.datetime.now())
    print("source:  %s/%s" % (os.getcwd(), os.path.basename(__file__)))
    print("\nModule Availability:")
    
    # Modules required for WorldCat functionality
    modules = {
        "re": "Regular Expression Module (Standard Library)",
        "requests": "HTTP Requests Library",
    }
    
    for module, description in modules.items():
        try:
            __import__(module)
            print(f"    {module}: Available - {description}")
        except ImportError:
            print(f"    {module}: NOT INSTALLED - {description}")
    print("=" * 40)

def process_bibfile(bibfile):
    """
    Process a .bib file to fetch and append WorldCat IDs based on ISBNs.
    
    Args:
        bibfile (str): Path to the .bib file.
    """
    WORLDCAT_API = "http://worldcat.org/webservices/catalog/content/isbn/{}?wskey=YOUR_API_KEY"

    # Read the .bib file
    try:
        with open(bibfile, "r") as file:
            entries = file.read()
    except FileNotFoundError:
        print(f"Error: File {bibfile} not found.")
        return

    # Extract ISBNs
    isbns = re.findall(r'isbn\s*=\s*{(\d+)}', entries)

    # Fetch WorldCat IDs and append them
    for isbn in isbns:
        print(f"Processing ISBN: {isbn}")
        response = requests.get(WORLDCAT_API.format(isbn))
        if response.status_code == 200:
            worldcat_id = re.search(r'<controlfield tag="001">(\d+)</controlfield>', response.text)
            if worldcat_id:
                worldcat_id = worldcat_id.group(1)
                print(f"Found WorldCat ID {worldcat_id} for ISBN {isbn}")
                # Append WorldCat ID to the entry (in-memory modification)
                entries = re.sub(f'isbn\s*=\s*{{{isbn}}}', f'isbn = {{{isbn}}},\n  worldcatid = {{{worldcat_id}}}', entries)
        else:
            print(f"Failed to fetch WorldCat ID for ISBN {isbn}: {response.status_code}")

    # Save the updated .bib file
    output_file = bibfile.replace(".bib", "_updated.bib")
    with open(output_file, "w") as file:
        file.write(entries)

    print(f"Updated .bib file saved to {output_file}")

def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python3 script.py <bibfile>")
        sys.exit(1)

    bibfile = sys.argv[1]
    pr_provenance()
    process_bibfile(bibfile)

if __name__ == "__main__":
    main()


