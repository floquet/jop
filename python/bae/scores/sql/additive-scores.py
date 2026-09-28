#!/usr/bin/env python3
"""Group source files by c0 + c1 + c2 + c3, from -4 through +4."""

import argparse
import datetime
import getpass
import platform
import sqlite3
import sys
from pathlib import Path


def print_provenance(database, output_dir):
    print("\n=== BASIC PROVENANCE ===")
    print(f"Timestamp: {datetime.datetime.now().astimezone().isoformat(timespec='seconds')}")
    print(f"User: {getpass.getuser()}")
    print(f"Script location: {Path(__file__).resolve()}")
    print(f"Working directory: {Path.cwd()}")
    print(f"Database: {database.resolve()}")
    print(f"Output directory: {output_dir.resolve()}")
    print("\n=== SYSTEM ===")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor() or platform.machine()}")
    print("\n=== PYTHON ===")
    print(f"• Version: {platform.python_version()}")
    print(f"• Executable: {sys.executable}")
    print(f"• Implementation: {platform.python_implementation()}")


def harvest(database, output_dir):
    if not database.is_file():
        raise FileNotFoundError(f"Database does not exist: {database}")

    # Open read-only so a bad path cannot silently create a new database.
    with sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True) as connection:
        rows = connection.execute("""
            SELECT source_file, c0, c1, c2, c3
            FROM scrape
            ORDER BY source_file
        """).fetchall()

    buckets = {score: [] for score in range(-4, 5)}
    incomplete = []
    for source_file, *scores in rows:
        if (not isinstance(source_file, str) or not source_file
                or any(type(score) is not int or score not in (-1, 0, 1)
                       for score in scores)):
            incomplete.append((source_file, scores))
            continue
        buckets[sum(scores)].append(source_file)

    output_dir.mkdir(parents=True, exist_ok=True)
    for total, files in buckets.items():
        filename = f"additive-score{total:+d}.txt"
        destination = output_dir / filename
        destination.write_text("".join(f"{source}\n" for source in files), encoding="utf-8")
        print(f"{total:+d}: {len(files):3d} files -> {destination}")

    incomplete_file = output_dir / "additive-score-incomplete.txt"
    incomplete_file.write_text(
        "".join(f"{source_file}\t{tuple(scores)}\n"
                for source_file, scores in incomplete), encoding="utf-8"
    )
    print(f"Incomplete/invalid: {len(incomplete)} -> {incomplete_file}")
    print(f"Records: {len(rows)} = {sum(map(len, buckets.values()))} scored "
          f"+ {len(incomplete)} incomplete/invalid")
    return buckets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path, help="Path to scrape.db")
    parser.add_argument("--output-dir", type=Path, default=Path.cwd(),
                        help="Where to write the text files (default: current directory)")
    args = parser.parse_args()
    try:
        harvest(args.database, args.output_dir)
    except (OSError, sqlite3.Error) as error:
        parser.exit(1, f"Error: {error}\n")
    # score vector for histogram
    print(f"sorted = {tuple(len(buckets[score]) for score in range(-4, 5))}")
    print_provenance(args.database, args.output_dir)


if __name__ == "__main__":
    main()

# dantopa@isomer:~/repos-isomer/github/jop/python/bae/scores/sql$ python3 additive_scores.py scrape.db 
# -4:   3 files -> /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/additive-score-4.txt
# -3:  15 files -> /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/additive-score-3.txt
# -2:   6 files -> /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/additive-score-2.txt
# -1:  12 files -> /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/additive-score-1.txt
# +0:   8 files -> /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/additive-score+0.txt
# +1:   2 files -> /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/additive-score+1.txt
# +2:   1 files -> /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/additive-score+2.txt
# +3:   3 files -> /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/additive-score+3.txt
# +4:   0 files -> /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/additive-score+4.txt
# Incomplete/invalid: 0 -> /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/additive-score-incomplete.txt
# Records: 50 = 50 scored + 0 incomplete/invalid

# === BASIC PROVENANCE ===
# Timestamp: 2026-09-27T20:51:58-06:00
# User: dantopa
# Script location: /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/additive_scores.py
# Working directory: /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql
# Database: /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql/scrape.db
# Output directory: /home/dantopa/repos-isomer/github/jop/python/bae/scores/sql

# === SYSTEM ===
# OS: Linux 7.0.11-76070011-generic
# Machine: x86_64
# Processor: x86_64

# === PYTHON ===
# • Version: 3.14.4
# • Executable: /usr/bin/python3
# • Implementation: CPython
# dantopa@isomer:~/repos-isomer/github/jop/python/bae/scores/sql$ 

