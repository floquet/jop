#!/usr/bin/env python3
import datetime
import getpass
import json
import platform
import sqlite3
import sys
from pathlib import Path


def harvest_json():
    directory = Path(__file__).resolve().parent / "scraped-json"
    database = directory / "scrape.db"
    loaded = 0
    skipped = 0

    with sqlite3.connect(database) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS scrape (
                source_file TEXT PRIMARY KEY,
                control_account TEXT,
                c0 INTEGER,
                c1 INTEGER,
                c2 INTEGER,
                c3 INTEGER
            )
        """)

        for path in sorted(directory.glob("*.json")):
            try:
                document = json.loads(path.read_text(encoding="utf-8"))
                metadata = document["metadata"]
                data = document["data"]
                scores = [area.get("score") for area in data.get("areas", [])]

                connection.execute("""
                    INSERT INTO scrape
                        (source_file, control_account, c0, c1, c2, c3)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(source_file) DO UPDATE SET
                        control_account = excluded.control_account,
                        c0 = excluded.c0,
                        c1 = excluded.c1,
                        c2 = excluded.c2,
                        c3 = excluded.c3
                """, (
                    metadata["source_file"],
                    data.get("control_account"),
                    data.get("score_overall"),
                    *(scores + [None] * 3)[:3],
                ))
                loaded += 1
                print(f"Loaded: {path.name}")

            except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
                skipped += 1
                print(f"Skipped {path.name}: {error}", file=sys.stderr)

    print(f"\nDatabase: {database}")
    print(f"Loaded: {loaded}; skipped: {skipped}")


# === PROVENANCE PRINTER ===
def print_provenance():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = getpass.getuser()
    script_path = Path(__file__).resolve()

    print("\n=== BASIC PROVENANCE ===")
    print(f"Timestamp: {current_time}")
    print(f"User: {user}")
    print(f"Script location: {script_path}")
    print(f"Working directory: {Path.cwd()}")

    print("\n=== SYSTEM ===")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")

    print("\n=== PYTHON ===")
    print(f"• Version: {platform.python_version()}")
    print(f"• Executable: {sys.executable}")
    print(f"• Implementation: {platform.python_implementation()}")


if __name__ == "__main__":
    harvest_json()
    print_provenance()