#!/usr/bin/env python3
# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# checktest.py
#
# Identification: tools/checktest.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""PA3 and PA4: check where your type checker reports errors.

    python3 tools/checktest.py test/pa3

Each program in a `bad` directory must be rejected at the line and column its
`# error: line:col` comment gives (columns count from 1). A few have two
errors; the comment gives the one that comes first in the file, which is the
one to report. Every other program must be accepted. Programs are
read with ast.parse unless you pass --parser=ours, so a PA2 bug does not
affect this test.
"""

import argparse
import sys
import traceback

from common import CPU_SECONDS, BadTest, OutOfTime, collect, cpu_limit, directives, summary

from compiler.errors import CompileError


def main() -> int:
    """
    @brief Run the command line; see the module's description.

    @return 0 if every test passes, else 1
    """
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--parser", choices=["python", "ours"], default="python")
    args = ap.parse_args()
    from compiler.__main__ import front_end

    results = []
    for path in collect(args.paths):
        source = path.read_text()
        try:
            expected = directives(source).error
        except BadTest as e:
            results.append(False)
            print(f"{'BAD TEST':9}{path}\n         {e}")
            continue
        detail = ""
        try:
            with cpu_limit():
                front_end(source, args.parser)
            ok = expected is None
            if not ok:
                detail = f"accepted, but expected an error at {expected[0]}:{expected[1]}"
        except CompileError as e:
            ok = expected == (e.line, e.col)
            if not ok:
                detail = (
                    f"error at {e.line}:{e.col}, expected {expected[0]}:{expected[1]}"
                    if expected
                    else "rejected a valid program"
                ) + f" ({e.message})"
        except OutOfTime:
            ok, detail = False, f"your checker used more than {CPU_SECONDS} s of CPU time"
        except Exception:
            ok, detail = False, "crashed:\n" + traceback.format_exc(limit=3)
        results.append(ok)
        print(f"{'ok' if ok else 'FAIL':9}{path}" + (f"\n         {detail}" if detail else ""))
    return summary(results, "tests")


if __name__ == "__main__":
    sys.exit(main())
