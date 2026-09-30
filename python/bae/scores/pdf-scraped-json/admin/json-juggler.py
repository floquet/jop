import json
from collections import Counter
from pathlib import Path

def classify_codes(input_dir):
    # Counters for the different levels of hierarchy
    major_code_counts = Counter()
    subcode_counts = Counter()
    
    # Path to the directory containing the JSON files
    path = Path(input_dir)
    files = sorted(path.glob("*.json"))
    
    if not files:
        print(f"No JSON files found in {input_dir}")
        return

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Extract the control account (e.g., "1.04.01.01")
                code = str(data.get("control_account", ""))
                if not code:
                    continue
                
                # Split the code by dots
                parts = code.split('.')
                
                if len(parts) >= 2:
                    # Generic Major Code: e.g., "1.04"
                    major = f"{parts[0]}.{parts[1]}"
                    major_code_counts[major] += 1
                    
                    # Generic Subcode: e.g., "1.04.01"
                    sub = f"{parts[0]}.{parts[1]}.{parts[2]}" if len(parts) >= 3 else major
                    subcode_counts[sub] += 1
                elif len(parts) == 1 and parts[0]:
                    # Fallback for codes that don't have dots
                    major = parts[0]
                    major_code_counts[major] += 1
                    subcode_counts[major] += 1

        except (json.JSONDecodeError, OSError) as e:
            print(f"Error processing {file_path.name}: {e}")

    # --- Reporting ---
    print("\n" + "="*30)
    print(f"CODE CLASSIFICATION REPORT")
    print("="*30)

    print("\n[Major Codes]")
    # Sort by code number (alphabetical/numerical)
    for code in sorted(major_code_counts.keys()):
        print(f"{code}: {major_code_counts[code]}")

    print("\n[Subcodes]")
    for sub in sorted(subcode_counts.keys()):
        print(f"{sub}: {subcode_counts[sub]}")
    
    print("="*30)

if __name__ == "__main__":
    # Update this path to your 'scraped-json' folder
    TARGET_DIR = "./scraped-json" 
    classify_codes(TARGET_DIR)


