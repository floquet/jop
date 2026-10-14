#!/usr/bin/env python3
"""List scrape records and load their four score columns as vectors."""

import argparse
import datetime
import getpass
import platform
import sqlite3
import sys
from pathlib import Path


def print_provenance():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n=== BASIC PROVENANCE ===")
    print(f"Timestamp: {current_time}")
    print(f"User: {getpass.getuser()}")
    print(f"Script location: {Path(__file__).resolve()}")
    print(f"Working directory: {Path.cwd()}")

    print("\n=== SYSTEM ===")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")

    print("\n=== PYTHON ===")
    print(f"• Version: {platform.python_version()}")
    print(f"• Executable: {sys.executable}")
    print(f"• Implementation: {platform.python_implementation()}")


def inspect_database(database: Path):
    # A read-only URI prevents a misspelled path from creating an empty database.
    if not database.is_file():
        raise FileNotFoundError(f"Database does not exist: {database}")

    with sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True) as connection:
        count = connection.execute("SELECT COUNT(*) FROM scrape").fetchone()[0]
        rows = connection.execute("""
            SELECT source_file, control_account, c0, c1, c2, c3
            FROM scrape
            ORDER BY source_file
        """).fetchall()

    print(f"Database: {database.resolve()}")
    print(f"Records: {count}")
    print("\n=== RECORDS ===")
    for number, (source, account, *scores) in enumerate(rows, start=1):
        print(f"{number}. {source}")
        print(f"   Control account: {account}")
        print(f"   Scores (c0, c1, c2, c3): {tuple(scores)}")

    # Each vector is aligned with the printed records, in source-file order.
    c0 = [row[2] for row in rows]
    c1 = [row[3] for row in rows]
    c2 = [row[4] for row in rows]
    c3 = [row[5] for row in rows]

    print("\n=== SCORE VECTORS ===")
    print(f"c0 = {c0}")
    print(f"c1 = {c1}")
    print(f"c2 = {c2}")
    print(f"c3 = {c3}")
    return c0, c1, c2, c3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path, help="Path to scrape.db")
    args = parser.parse_args()
    try:
        inspect_database(args.database)
    except (OSError, sqlite3.Error) as error:
        parser.exit(1, f"Error: {error}\n")
    print_provenance()


if __name__ == "__main__":
    main()
