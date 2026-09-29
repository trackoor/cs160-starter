#!/usr/bin/env python3
# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# difftest.py
#
# Identification: tools/difftest.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""Differential testing: run each program under CPython and as a binary built by
your compiler, and compare what they print and whether they fail.

    python3 tools/difftest.py test/pa1                 all tests in a directory
    python3 tools/difftest.py test/mine/pa1/loop.py    one test
    python3 tools/difftest.py -O1 --verify test/pa5    with your PA5 passes

Options -O1, -O2, --verify and --parser are passed to the compiler. A test
passes when your program prints exactly CPython's output and succeeds or fails
as CPython does; see tools/common.py for the comment lines that change what is
expected. `# ir-has` and `# ir-lacks` lines are checked against the IR at the
level you choose, so run the PA5 tests with -O1 and the PA6 tests with -O2. A
program may use 10 s of CPU time; a timeout is reported as TIMEOUT, never as a pass.
"""

import argparse
import os
import re
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import (
    COMPILE_CPU_SECONDS,
    COMPILE_WALL_SECONDS,
    CPU_SECONDS,
    ROOT,
    BadTest,
    collect,
    crash,
    directives,
    run_limited,
    summary,
)


def compiler_command(args, command, path, extra=()):
    """
    @brief Build the command line that runs your compiler.

    @param args the parsed options, passed on to the compiler
    @param command the compiler's command, such as "build"
    @param path the program
    @param extra more arguments
    @return the command
    """
    cmd = [sys.executable, "-m", "compiler", command, str(path)]
    if args.level:
        cmd.append(f"-O{args.level}")
    if args.verify:
        cmd.append("--verify")
    if args.parser:
        cmd.append(f"--parser={args.parser}")
    return cmd + list(extra)


def run_test(path: Path, args) -> tuple[str, str]:
    """
    @brief Compare one program under CPython and under your compiler.

    @param path the program
    @param args the parsed options
    @return (status, detail): "ok", "FAIL", "TIMEOUT" or "BAD TEST", and why
    """
    source = path.read_text()
    try:
        d = directives(source)
    except BadTest as e:
        return "BAD TEST", str(e)
    if d.error:
        return "BAD TEST", "it expects a compile error (# error:), so put it in a bad/ directory"
    if d.cpython_differs:
        expected_out = "".join(line + "\n" for line in d.expect_stdout)
        expected_fail = d.expect_exit is not None and d.expect_exit != 0
    else:
        ref = run_limited([sys.executable, str(path)])
        if ref is None:
            return "TIMEOUT", "CPython did not finish"
        expected_out, expected_fail = ref.stdout, ref.returncode != 0
        if d.expect_exit and not expected_fail:
            return "BAD TEST", "CPython succeeded, but the test expects an error"
        if expected_fail and d.expect_exit is None:
            return "BAD TEST", "CPython stops with an error; a test that should fail needs an # expect-exit line"

    with tempfile.TemporaryDirectory() as tmp:
        exe = str(Path(tmp) / "prog")
        built = run_limited(
            compiler_command(args, "build", path, ["-o", exe]), COMPILE_CPU_SECONDS, COMPILE_WALL_SECONDS, cwd=ROOT
        )
        if built is None:
            return "TIMEOUT", f"your compiler used more than {COMPILE_CPU_SECONDS} s of CPU time"
        if built.returncode:
            lines = built.stderr.strip().splitlines() or ["(no message)"]
            # When clang rejects the IR, its first error says why; otherwise the last line does.
            clang = next((line for line in lines if re.search(r"(^|\s)error: ", line)), None)
            return "FAIL", f"does not compile: {clang or lines[-1]}"
        ours = run_limited([exe])
        if ours is None:
            return "TIMEOUT", f"your program used more than {CPU_SECONDS} s of CPU time"

    if crash(ours.returncode):
        lines = len(ours.stdout.splitlines())
        return "FAIL", f"your program crashed after printing {lines} line(s): {crash(ours.returncode)}"
    if ours.stdout != expected_out:
        want = expected_out.splitlines()
        got = ours.stdout.splitlines()
        for i in range(max(len(want), len(got))):
            w = want[i] if i < len(want) else "(no more output)"
            g = got[i] if i < len(got) else "(no more output)"
            if w != g:
                return "FAIL", f"output line {i + 1}: expected {w!r}, got {g!r}"
    failed = ours.returncode != 0
    if failed != expected_fail:
        what = f"stopped with exit code {ours.returncode}" if failed else "finished normally"
        return "FAIL", f"your program {what}, but it should {'fail' if expected_fail else 'finish normally'}"
    if d.expect_exit is not None and ours.returncode != d.expect_exit:
        return "FAIL", f"exit code {ours.returncode}, expected {d.expect_exit}"
    if d.ir_has or d.ir_lacks or d.ir_count:
        printed = run_limited(compiler_command(args, "ll", path), COMPILE_CPU_SECONDS, COMPILE_WALL_SECONDS, cwd=ROOT)
        if printed is None:
            return "TIMEOUT", f"your compiler used more than {COMPILE_CPU_SECONDS} s of CPU time"
        ir = printed.stdout
        for pattern in d.ir_has:
            if not re.search(pattern, ir, re.M):
                return "FAIL", f"the IR should match {pattern!r}"
        for pattern in d.ir_lacks:
            if re.search(pattern, ir, re.M):
                return "FAIL", f"the IR should not match {pattern!r}"
        for pattern, n in d.ir_count:
            found = len(re.findall(pattern, ir, re.M))
            if found != n:
                return "FAIL", f"the IR matches {pattern!r} {found} times, expected {n}"
    return "ok", ""


def main() -> int:
    """
    @brief Run the command line; see the module's description.

    @return 0 if every test passes, else 1
    """
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("-O", dest="level", type=int, choices=[0, 1, 2], default=0)
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--parser", choices=["python", "ours"])
    ap.add_argument("-j", "--jobs", type=int, default=os.cpu_count() or 2)
    args = ap.parse_args()
    files = collect(args.paths, bad=False)
    if not files:
        if collect(args.paths, bad=True):
            print("no tests found: a program in a bad/ directory must be rejected; check it with checktest.py")
        else:
            print("no tests found")
        return 1
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        outcomes = list(pool.map(lambda f: run_test(f, args), files))
    for f, (status, detail) in zip(files, outcomes):
        print(f"{status:9}{f}" + (f"\n         {detail}" if detail else ""))
    return summary([status == "ok" for status, _ in outcomes], "tests")


if __name__ == "__main__":
    sys.exit(main())
