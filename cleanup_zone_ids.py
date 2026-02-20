#!/usr/bin/env python3
"""Delete all Zone.Identifier files recursively, skipping venv directories."""

import os
import sys

VENV_DIRS = {"venv", "env", ".venv", ".env"}


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    root = os.path.abspath(root)
    deleted = 0
    dirs_affected = {}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in VENV_DIRS]

        for name in filenames:
            if name.endswith(":Zone.Identifier"):
                path = os.path.join(dirpath, name)
                os.remove(path)
                dirs_affected[dirpath] = dirs_affected.get(dirpath, 0) + 1
                deleted += 1

    if dirs_affected:
        print("Directories cleaned:")
        for d, count in dirs_affected.items():
            print(f"  {d} ({count})")
        print(f"\n{deleted} file(s) deleted across {len(dirs_affected)} directory(ies).")
    else:
        print("No Zone.Identifier files found.")


if __name__ == "__main__":
    main()
