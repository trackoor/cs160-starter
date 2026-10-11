#!/usr/bin/env python3
# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# parsetest.py
#
# Identification: tools/parsetest.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""PA2: compare your parser with Python's ast.parse.

    python3 tools/parsetest.py test/pa2

For each valid program, your tree must print the same `ast.dump` as ast.parse's,
and every statement, expression and function parameter must start at the same
line and column.
For each program in a `bad` directory, your parser must report an error at the
position its `# error: line:col` comment gives (columns count from 1).
"""

import argparse
import ast
import sys
import traceback

from common import CPU_SECONDS, BadTest, OutOfTime, collect, cpu_limit, directives, summary

from compiler.__main__ import dump, read_program
from compiler.errors import CompileError


def first_position_difference(ours, theirs):
    """
    @brief Find the first node whose position differs from ast.parse's.

    @param ours your tree
    @param theirs the tree ast.parse built
    @return a description of the difference, or None
    """
    for a, b in zip(ast.walk(ours), ast.walk(theirs)):
        if isinstance(b, (ast.stmt, ast.expr, ast.arg)):
            pa = (getattr(a, "lineno", None), getattr(a, "col_offset", None))
            pb = (b.lineno, b.col_offset)
            if pa != pb:
                return f"{type(b).__name__} should start at {pb[0]}:{pb[1] + 1}, yours starts at " + (
                    f"{pa[0]}:{pa[1] + 1}" if None not in pa else "no position"
                )
    return None


def check_valid(path, parse):
    """
    @brief Check your parser on a valid program.

    @param path the program
    @param parse your parse function
    @return (passed, detail)
    """
    source = path.read_text()
    try:
        if directives(source).error is not None:
            return False, "bad test: a test with # error: belongs in a bad/ directory"
    except BadTest as e:
        return False, f"bad test: {e}"
    try:
        expected = ast.parse(source)
    except SyntaxError as e:
        return False, f"bad test: Python rejects it at {e.lineno}:{e.offset} ({e.msg}); put it in a bad/ directory"
    try:
        with cpu_limit():
            ours = parse(source)
    except OutOfTime:
        return False, f"your parser used more than {CPU_SECONDS} s of CPU time"
    except CompileError as e:
        return False, f"rejected a valid program: {e}"
    except Exception:
        return False, "crashed:\n" + traceback.format_exc(limit=3)
    try:
        if dump(ours) != dump(expected):
            a, b = dump(ours), dump(expected)
            i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
            return (
                False,
                f"different tree near:\n           yours:    ...{a[max(0, i - 40) : i + 40]}..."
                f"\n           ast.parse: ...{b[max(0, i - 40) : i + 40]}...",
            )
        difference = first_position_difference(ours, expected)
        if difference:
            return False, difference
        return True, ""
    except Exception:
        return False, "crashed while inspecting your tree:\n" + traceback.format_exc(limit=3)


def check_invalid(path, parse):
    """
    @brief Check that your parser rejects a program at the position its comment gives.

    @param path the program
    @param parse your parse function
    @return (passed, detail)
    """
    source = path.read_text()
    try:
        expected = directives(source).error
    except BadTest as e:
        return False, f"bad test: {e}"
    if expected is None:
        return False, "the test has no '# error: line:col' comment"
    try:
        with cpu_limit():
            parse(source)
    except OutOfTime:
        return False, f"your parser used more than {CPU_SECONDS} s of CPU time"
    except CompileError as e:
        if (e.line, e.col) == expected:
            return True, ""
        return False, f"error at {e.line}:{e.col}, expected {expected[0]}:{expected[1]} ({e.message})"
    except Exception:
        return False, "crashed:\n" + traceback.format_exc(limit=3)
    return False, "accepted a program that must be rejected"


def main() -> int:
    """
    @brief Run the command line; see the module's description.

    @return 0 if every test passes, else 1
    """
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    args = ap.parse_args()

    def parse(source):
        return read_program(source, "ours")  # your parser, with the fields it may omit filled in

    results = []
    for path in collect(args.paths):
        ok, detail = (check_invalid if "bad" in path.parts else check_valid)(path, parse)
        results.append(ok)
        print(f"{'ok' if ok else 'FAIL':9}{path}" + (f"\n         {detail}" if detail else ""))
    return summary(results, "tests")


if __name__ == "__main__":
    sys.exit(main())
