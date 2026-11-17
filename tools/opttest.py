#!/usr/bin/env python3
# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# opttest.py
#
# Identification: tools/opttest.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""PA5 and PA6: run your passes on the reference compiler's IR.

    python3 tools/opttest.py -O1 test/pa5
    python3 tools/opttest.py -O2 test/pa6

Each test is a pair: prog.py (the program) and prog.ll (the reference
compiler's IR for it). In test/pa5 the .ll is the IR before any optimization,
and -O1 runs your SSA construction and local optimizations on it. In test/pa6
the .ll is already in SSA form, produced by the reference PA5 passes, and -O2
runs only your global optimizer on it. The tool runs your passes with --verify,
checks the IR against the `# ir-...` comments in prog.py, builds and runs the
result, and compares the output with CPython. Graders use the same inputs, so
a bug in an earlier assignment cannot affect these tests.

The comment lines are those of tools/common.py; here `# ir-has`, `# ir-lacks`
and `# ir-count` are checked against the optimized IR.
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from common import (
    COMPILE_CPU_SECONDS,
    COMPILE_WALL_SECONDS,
    CPU_SECONDS,
    ROOT,
    BadTest,
    clang,
    collect,
    crash,
    directives,
    run_limited,
    summary,
)

RUNTIME = ROOT / "runtime" / "runtime.c"


def run_test(py: Path, level: int) -> tuple[str, str]:
    """
    @brief Run your passes on one test's reference IR, check the result, and run it.

    @param py the test program; its IR is the .ll file next to it
    @param level 1 for your PA5 passes, 2 for your PA6 pass
    @return (status, detail): "ok", "FAIL", "TIMEOUT" or "BAD TEST", and why
    """
    ll = py.with_suffix(".ll")
    if not ll.exists():
        return "BAD TEST", f"{ll.name} is missing"
    source = py.read_text()
    try:
        d = directives(source)
    except BadTest as e:
        return "BAD TEST", str(e)
    passes = ["-O1"] if level == 1 else ["--passes=global"]
    opt = run_limited(
        [sys.executable, "-m", "compiler", "opt", *passes, "--verify", str(ll)],
        COMPILE_CPU_SECONDS,
        COMPILE_WALL_SECONDS,
        cwd=ROOT,
    )
    if opt is None:
        return "TIMEOUT", f"your passes used more than {COMPILE_CPU_SECONDS} s of CPU time"
    if opt.returncode:
        return "FAIL", (opt.stderr.strip().splitlines() or ["your passes failed"])[-1]
    ir = opt.stdout
    for pattern in d.ir_has:
        if not re.search(pattern, ir, re.M):
            return "FAIL", f"the optimized IR should match {pattern!r}"
    for pattern in d.ir_lacks:
        if re.search(pattern, ir, re.M):
            return "FAIL", f"the optimized IR should not match {pattern!r}"
    for pattern, n in d.ir_count:
        found = len(re.findall(pattern, ir, re.M))
        if found != n:
            return "FAIL", f"the optimized IR matches {pattern!r} {found} times, expected {n}"
    if d.cpython_differs:
        expected_out = "".join(line + "\n" for line in d.expect_stdout)
        expected_fail = bool(d.expect_exit)
    else:
        ref = run_limited([sys.executable, str(py)])
        if ref is None:
            return "TIMEOUT", "CPython did not finish"
        expected_out, expected_fail = ref.stdout, ref.returncode != 0
        if expected_fail and d.expect_exit is None:
            return "BAD TEST", "CPython stops with an error; a test that should fail needs an # expect-exit line"
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "opt.ll").write_text(ir)
        exe = Path(tmp) / "prog"
        built = subprocess.run(
            [clang(), "-O0", "-w", "-Wno-override-module", "-o", str(exe), str(Path(tmp) / "opt.ll"), str(RUNTIME)],
            capture_output=True,
            text=True,
        )
        if built.returncode:
            return "FAIL", "clang rejected the optimized IR: " + (built.stderr.strip().splitlines() or [""])[0]
        ours = run_limited([str(exe)])
        if ours is None:
            return "TIMEOUT", f"the optimized program used more than {CPU_SECONDS} s of CPU time"
    if crash(ours.returncode):
        return "FAIL", f"the optimized program crashed: {crash(ours.returncode)}"
    if ours.stdout != expected_out:
        return "FAIL", "the optimized program prints something different"
    if (ours.returncode != 0) != expected_fail or (d.expect_exit is not None and ours.returncode != d.expect_exit):
        return "FAIL", f"the optimized program exits with {ours.returncode}"
    return "ok", ""


def main() -> int:
    """
    @brief Run the command line; see the module's description.

    @return 0 if every test passes, else 1
    """
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("-O", dest="level", type=int, choices=[1, 2], required=True)
    args = ap.parse_args()
    results = []
    for py in collect(args.paths, bad=False):
        status, detail = run_test(py, args.level)
        results.append(status == "ok")
        print(f"{status:9}{py}" + (f"\n         {detail}" if detail else ""))
    return summary(results, "tests")


if __name__ == "__main__":
    sys.exit(main())
