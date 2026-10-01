#!/usr/bin/env python3
# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# doctor.py
#
# Identification: tools/doctor.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""Check that this machine can run the course tools.

    python3 tools/doctor.py

It shows your Python version, finds clang, compiles and runs a small LLVM IR
program together with the course runtime, and runs the compiler on
`print(160)`. Run it once after setting up, and again whenever something
fails for reasons that do not look like your code.
"""

import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Uses opaque pointers (`ptr`), which need LLVM 15 or later.
PROGRAM = """declare void @cp_print_int(i32)
declare ptr @cp_alloc(i64)

define i32 @main() {
entry:
  %p = call ptr @cp_alloc(i64 4)
  store i32 160, ptr %p
  %v = load i32, ptr %p
  call void @cp_print_int(i32 %v)
  ret i32 0
}
"""


def main() -> int:
    """
    @brief Run every check and report the problems found.

    @return 0 if the machine is ready, else 1
    """
    problems = 0

    def report(passed: bool, what: str, advice: str = "") -> None:
        nonlocal problems
        print(f"{'ok' if passed else 'FAIL':6}{what}")
        if not passed:
            problems += 1
            if advice:
                print(f"      {advice}")

    # No version or system is refused here: the checks below run the real tools, and fail only if they do.
    report(True, f"Python {platform.python_version()} at {sys.executable}, on {platform.system()}")

    cc = os.environ.get("CC") or shutil.which("clang")
    report(cc is not None, f"clang found at {cc}" if cc else "clang not found", "install clang; see Setup in README.md")
    if cc:
        version = subprocess.run([cc, "--version"], capture_output=True, text=True).stdout.splitlines()
        print(f"      {version[0] if version else '(no version line)'}")
        with tempfile.TemporaryDirectory() as tmp:
            ll, exe = Path(tmp) / "check.ll", Path(tmp) / "check"
            ll.write_text(PROGRAM)
            built = subprocess.run(
                [cc, "-O0", "-w", "-Wno-override-module", "-o", str(exe), str(ll), str(ROOT / "runtime" / "runtime.c")],
                capture_output=True,
                text=True,
            )
            if built.returncode:
                first = (built.stderr.strip().splitlines() or [""])[0]
                report(
                    False,
                    "clang compiles LLVM IR with the course runtime",
                    f"{first}\n      (this clang is too old to read the course's IR: on Linux, run"
                    " build_support/packages.sh, which installs a newer one;\n      on macOS, update the Xcode"
                    " command-line tools)",
                )
            else:
                ran = subprocess.run([str(exe)], capture_output=True, text=True, timeout=10)
                report(ran.stdout == "160\n", "clang compiles LLVM IR with the course runtime, and it runs")

    ruff = ROOT / "build_support" / ".venv" / "bin" / "ruff"
    found_ruff = ruff if ruff.exists() else shutil.which("ruff")
    print(
        f"{'ok' if found_ruff else 'note':6}"
        + (
            f"ruff found at {found_ruff}"
            if found_ruff
            else "ruff not found: `make format` and `make check-lint` need it; build_support/packages.sh installs it"
        )
    )

    with tempfile.TemporaryDirectory() as tmp:
        hello = Path(tmp) / "hello.py"
        hello.write_text("print(160)\n")
        ran = subprocess.run(
            [sys.executable, "-m", "compiler", "run", "--parser=python", str(hello)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        last = (ran.stderr.strip().splitlines() or ["(no message)"])[-1]
        report(ran.stdout == "160\n", "python3 -m compiler run hello.py prints 160", last)

    print("\nAll set." if problems == 0 else "\nFix the problems above, then run this again.")
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
