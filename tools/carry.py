#!/usr/bin/env python3
# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# carry.py
#
# Identification: tools/carry.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""Bring your work from the folder of an earlier assignment into this one.

    python3 tools/carry.py ../cs160-pa1

Each assignment's `oneworld assessment join` downloads its starter code into a
new folder. Run this in the new folder, with the folder of your previous
assignment, to copy what you wrote there:

  - the modules of compiler/ that you write (codegen.py, lexer.py, ...), and
    any module you added to compiler/;
  - your tests, test/mine/;
  - your design documents, docs/pa*-design.md.

It never copies a file the course provides, since the new starter may have a
newer one. If a file it would copy already differs here from the starter, it
copies nothing, so that it cannot overwrite work you did in this folder;
--force copies anyway.
"""

import argparse
import filecmp
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The modules of compiler/ that the course provides; every other module there is yours.
PROVIDED = {"__init__.py", "__main__.py", "config.py", "emit.py", "errors.py", "ir.py", "subset.py"}


def yours(folder: Path) -> list[Path]:
    """
    @brief Find the files to carry.

    @param folder the folder of an earlier assignment
    @return the paths of your files in it, relative to it
    """
    files = [p for p in (folder / "compiler").glob("*.py") if p.name not in PROVIDED]
    files += [p for p in (folder / "test" / "mine").rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    files += (folder / "docs").glob("pa*-design.md")
    return sorted(p.relative_to(folder) for p in files)


def starter_version(rel: Path) -> bytes | None:
    """
    @brief Get a file as the starter had it: in the first commit of this folder, which `join` made.

    @param rel a path relative to this folder
    @return the file's content, or None if the starter did not have it or this folder has no history
    """

    def git(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True)

    first = git("rev-list", "--max-parents=0", "HEAD").stdout.split()
    if not first:
        return None
    shown = git("show", f"{first[-1].decode()}:{rel.as_posix()}")
    return shown.stdout if shown.returncode == 0 else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", type=Path, help="the folder of your previous assignment")
    ap.add_argument("--force", action="store_true", help="overwrite files that you already changed here")
    args = ap.parse_args()
    folder = args.folder.expanduser().resolve()
    if not (folder / "compiler").is_dir():
        sys.exit(f"{args.folder} has no compiler/ folder: give the folder of your previous assignment.")
    if folder == ROOT:
        sys.exit("That is this folder: give the folder of your previous assignment.")

    todo, mine_here = [], []
    for rel in yours(folder):
        here = ROOT / rel
        if here.exists() and filecmp.cmp(folder / rel, here, shallow=False):
            continue  # already the same
        if here.exists() and starter_version(rel) != here.read_bytes():
            mine_here.append(rel)
        todo.append(rel)
    if mine_here and not args.force:
        print("Nothing was copied. These files already differ here from the starter, and carrying would")
        print("overwrite them:")
        for rel in mine_here:
            print(f"  {rel.as_posix()}")
        print("Run again with --force to overwrite them.")
        return 1
    for rel in todo:
        (ROOT / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(folder / rel, ROOT / rel)
        print(f"copied {rel.as_posix()}")
    print(f"Copied {len(todo)} file{'' if len(todo) == 1 else 's'} from {args.folder}.", end=" ")
    print("Run `make check-tests` to see that your earlier work still passes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
