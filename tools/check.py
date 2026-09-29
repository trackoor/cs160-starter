#!/usr/bin/env python3
# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# check.py
#
# Identification: tools/check.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""Run the local tests of every released assignment with one command.

    python3 tools/check.py            every released assignment, and your tests in test/mine
    python3 tools/check.py pa3        one assignment

Each line is one suite: a tool from the handouts, run on the staff's public
tests or on your own tests in test/mine/paN. Failing tests are listed under
their suite. To see why one failed, run the command shown on its suite line.
"""

import argparse
import re
import subprocess
import sys

from common import ROOT, collect

sys.path.insert(0, str(ROOT))
from compiler import config  # noqa: E402

SHOWN_FAILURES = 8


def suites(pa: int) -> list[list[str]]:
    """
    @brief List the tool runs for one assignment, as the writeups describe them.

    @param pa the assignment's number
    @return the runs, each a tool and its arguments
    """
    tests = []
    for where in (f"test/pa{pa}", f"test/mine/pa{pa}"):
        if pa == 1:
            tests.append(["difftest.py", where])
        elif pa == 2:
            tests.append(["parsetest.py", where])
        elif pa in (3, 4):  # with Python's parser, as graded, so that a PA2 bug does not count twice
            tests += [["checktest.py", "--parser=python", where], ["difftest.py", "--parser=python", where]]
        elif pa == 5:
            if where.startswith("test/pa"):
                tests.append(["opttest.py", "-O1", where])
            tests.append(["difftest.py", "-O1", "--verify", where])
        else:
            if where.startswith("test/pa"):
                tests.append(["opttest.py", "-O2", where])
            tests.append(["difftest.py", "-O2", "--verify", where])
    return tests


def count(tool: str, where: str) -> int:
    """
    @brief Count the test programs a tool would run in a directory.

    @param tool the tool's file name
    @param where the directory
    @return the number of programs
    """
    path = ROOT / where
    if not path.is_dir():
        return 0
    return len(collect([str(path)], bad=False if tool in ("difftest.py", "opttest.py") else None))


def main() -> int:
    """
    @brief Run the command line; see the module's description.

    @return 0 if every suite passes, else 1
    """
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("assignments", nargs="*", help="pa1 ... pa6 (default: every released one)")
    args = ap.parse_args()
    released = list(range(1, config.RELEASED + 1))
    chosen = []
    for name in args.assignments or [f"pa{n}" for n in released]:
        m = re.fullmatch(r"(?i)pa([1-6])", name)
        if not m:
            ap.error(f"unknown assignment {name!r}; use pa1 ... pa6")
        if int(m.group(1)) not in released:
            ap.error(f"{name} has not been released yet")
        chosen.append(int(m.group(1)))

    all_passed = True
    untested = []  # the test/mine directories that are still empty
    for pa in chosen:
        empty_reported = set()
        for run in suites(pa):
            tool, where = run[0], run[-1]
            command = "python3 tools/" + " ".join(run)
            if count("any", where) == 0:
                if where not in empty_reported:
                    empty_reported.add(where)
                    if "mine" in where:
                        untested.append(where)
                    print(
                        f"PA{pa}  {where + '/':<52} no tests yet"
                        + (" (the handout asks for three)" if "mine" in where else "")
                    )
                continue
            if count(tool, where) == 0:
                continue  # for example, only bad/ programs, which difftest does not run
            result = subprocess.run(
                [sys.executable, str(ROOT / "tools" / tool), *run[1:]], cwd=ROOT, capture_output=True, text=True
            )
            summary = re.search(r"^(\d+)/(\d+) tests passed$", result.stdout, re.M)
            if summary is None:
                all_passed = False
                reason = (result.stderr.strip().splitlines() or ["no summary"])[-1]
                print(f"PA{pa}  {command:<52} the tool failed: {reason}")
                continue
            passed, total = int(summary.group(1)), int(summary.group(2))
            all_passed &= passed == total
            print(f"PA{pa}  {command:<52} {passed}/{total} passed")
            failures = [
                line.split(None, 1)[1]
                for line in result.stdout.splitlines()
                if line.startswith(("FAIL", "TIMEOUT", "BAD TEST"))
            ]
            for name in failures[:SHOWN_FAILURES]:
                print(f"       failed: {name.replace('TEST', '').strip()}")
            if len(failures) > SHOWN_FAILURES:
                print(f"       ... and {len(failures) - SHOWN_FAILURES} more")
    if not all_passed:
        print("\nSome tests fail; run the commands above for details.")
    elif untested:
        print(f"\nEverything passes, but {' and '.join(untested)} has no tests of your own yet.")
    else:
        print("\nEverything passes.")
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
