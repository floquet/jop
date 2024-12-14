import os
import re

def repair_bibtex_files ( directory ) :
    """Scan and repair .bib files by escaping '%' in 'abstract' fields."""
    if not os.path.isdir ( directory ) :
        raise ValueError ( f"Provided path '{directory}' is not a valid directory." ) 

    # Regex pattern to match abstract fields
    abstract_pattern = re.compile ( r" ( abstract\s*=\s*{.*?[^\\]}|abstract\s*=\s*\".*?[^\\]\" ) ", re.DOTALL ) 

    for root, _, files in os.walk ( directory ) :
        for file in files:
            if file.endswith ( '.bib' ) :
                file_path = os.path.join ( root, file ) 
                print ( f"Processing: {file_path}" ) 
                
                # Read the file
                with open ( file_path, 'r', encoding='utf-8' )  as f:
                    content = f.read (  ) 

                # Repair abstract fields
                def escape_percent ( match ) :
                    field = match.group ( 0 ) 
                    # Escape '%' not already escaped
                    return re.sub ( r" ( ?<!\\ ) %", r"\\%", field ) 

                new_content = abstract_pattern.sub ( escape_percent, content ) 

                # Save the file only if changes were made
                if new_content != content:
                    with open ( file_path, 'w', encoding='utf-8' )  as f:
                        f.write ( new_content ) 
                    print ( f"Repaired: {file_path}" ) 
                else:
                    print ( f"No changes needed: {file_path}" ) 

# Specify the directory containing your .bib files
directory = "/Users/dantopa/repos-xiuhcoatal/github/sharing/bibliographies"

try:
    repair_bibtex_files ( directory ) 
except Exception as e:
    print ( f"Error: {e}" ) 

    """Print system provenance."""
    print("\nExecution Provenance")
    print("=" * 40)
    print("\n", datetime.datetime.now())
    print("source:  %s/%s" % (os.getcwd(), os.path.basename(__file__)))
    print("user id:", pwd.getpwuid(os.getuid()).pw_name)
    print("platform info:")
    print("    platform: ", platform.platform())
    print("    uname:    ", platform.uname())
    print("version info:")
    print("    python:   %s" % sys.version)
    print("    numpy:   ", np.__version__)
    print("    pandas:  ", pd.__version__)
    print("    matplotlib: ", plt.matplotlib.__version__)
    print("=" * 40)

