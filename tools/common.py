# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# common.py
#
# Identification: tools/common.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""Helpers shared by the test tools.

A test is a ChocoPy program. By default CPython is its answer key. Comment
lines at its top state what to expect when CPython is not the right answer
key, or add checks:

    # expect-exit: 3            the program must stop with this ChocoPy exit code
    # cpython-differs           do not run CPython; the expect-stdout lines give the output
    # expect-stdout: 1          one line of expected output (repeat for more lines)
    # error: 4:12               the compiler must reject the program at line 4, column 12
    # ir-has: call .*@cp_error  a regular expression the IR must match
    # ir-lacks: alloca          a regular expression the IR must not match
    # ir-count: = phi 3         the IR must match a regular expression exactly this often
"""

import os
import re
import shutil
import signal
import subprocess
import sys
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# A test program may use this much CPU time, and your compiler this much on one test.
# The real-time limits are far larger, so a busy machine (or macOS checking a new
# binary before its first launch) never turns a correct program into a timeout.
CPU_SECONDS = 10
WALL_SECONDS = 60
COMPILE_CPU_SECONDS = 60
COMPILE_WALL_SECONDS = 300


def run_limited(
    command: list[str], cpu: int = CPU_SECONDS, wall: int = WALL_SECONDS, cwd: Path | None = None
) -> subprocess.CompletedProcess | None:
    """Run a command with a CPU-time limit; None if it ran out of time."""
    limited = ["/bin/sh", "-c", f'ulimit -t {cpu} && exec "$0" "$@"', *command]
    try:
        result = subprocess.run(limited, cwd=cwd, capture_output=True, text=True, timeout=wall)
    except subprocess.TimeoutExpired:
        return None
    if result.returncode in (-signal.SIGXCPU, -signal.SIGKILL, 128 + signal.SIGXCPU):
        return None
    return result


class OutOfTime(BaseException):
    """Raised inside `cpu_limit`. A BaseException, so `except Exception` cannot swallow it."""


@contextmanager
def cpu_limit(seconds: int = CPU_SECONDS):
    """Stop the code in the block with OutOfTime after `seconds` of CPU time (main thread only)."""

    def expired(signum, frame):
        raise OutOfTime()

    previous = signal.signal(signal.SIGPROF, expired)
    signal.setitimer(signal.ITIMER_PROF, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_PROF, 0)
        signal.signal(signal.SIGPROF, previous)


def clang() -> str:
    """The C compiler to use: $CC if set (for example CC=clang-15), else clang."""
    found = os.environ.get("CC") or shutil.which("clang")
    if not found:
        sys.exit("clang was not found; see Setup in README.md, or run python3 tools/doctor.py")
    return found


@dataclass
class Directives:
    expect_exit: int | None = None
    cpython_differs: bool = False
    expect_stdout: list[str] = field(default_factory=list)
    error: tuple[int, int] | None = None
    ir_has: list[str] = field(default_factory=list)
    ir_lacks: list[str] = field(default_factory=list)
    ir_count: list[tuple[str, int]] = field(default_factory=list)


class BadTest(ValueError):
    """A test whose directives cannot be read; the tools report it as BAD TEST."""


def directives(source: str) -> Directives:
    """
    @brief Read the comment lines that state what a test expects.

    @param source the test program
    @return its directives
    @throws BadTest if a directive's value has the wrong form, for example `# error: 4`, or if
        `# expect-stdout` appears without `# cpython-differs`
    """
    d = Directives()
    for number, line in enumerate(source.splitlines(), 1):
        m = re.match(r"\s*#\s*([a-z-]+)\s*(?::\s?(.*))?$", line)
        if not m:
            continue
        key, value = m.group(1), (m.group(2) or "").rstrip("\n")
        if key == "expect-exit":
            if not re.fullmatch(r"\s*\d+\s*", value):
                raise BadTest(f"line {number}: '# expect-exit:' needs an exit code, for example '# expect-exit: 3'")
            d.expect_exit = int(value)
        elif key == "cpython-differs":
            d.cpython_differs = True
        elif key == "expect-stdout":
            d.expect_stdout.append(value)
        elif key == "error":
            position = re.fullmatch(r"\s*(\d+)\s*:\s*(\d+)\s*", value)
            if not position:
                raise BadTest(f"line {number}: '# error:' needs a line:col position, for example '# error: 4:12'")
            d.error = (int(position.group(1)), int(position.group(2)))
        elif key == "ir-has":
            d.ir_has.append(value)
        elif key == "ir-lacks":
            d.ir_lacks.append(value)
        elif key == "ir-count":
            count = re.fullmatch(r"(.*\S)\s+(\d+)\s*", value)
            if not count:
                example = "for example '# ir-count: = phi 3'"
                raise BadTest(f"line {number}: '# ir-count:' needs a pattern and a count, {example}")
            d.ir_count.append((count.group(1), int(count.group(2))))
    if d.expect_stdout and not d.cpython_differs:
        raise BadTest("'# expect-stdout:' counts only with '# cpython-differs'; otherwise CPython gives the output")
    return d


# What each crash usually means in a compiled ChocoPy program.
CRASHES = {
    signal.SIGSEGV: "a bad memory access, such as a missing check or a wrong address",
    signal.SIGBUS: "a bad memory access, such as a missing check or a wrong address",
    signal.SIGFPE: "an arithmetic trap, such as a division by zero with no check",
    signal.SIGILL: "an illegal instruction, such as an `unreachable` that was reached, on some machines",
    signal.SIGTRAP: "a trap, such as an `unreachable` that was reached, on some machines",
    signal.SIGABRT: "an abort",
}


def crash(returncode: int) -> str | None:
    """
    @brief Describe how a program crashed.

    @param returncode the program's return code from subprocess
    @return the signal that killed it and what that usually means, or None if no signal did
    """
    if returncode >= 0:
        return None
    try:
        sig = signal.Signals(-returncode)
    except ValueError:
        return f"signal {-returncode}"
    return f"{sig.name}: {CRASHES.get(sig, 'killed by a signal')}"


def collect(paths: list[str], bad: bool | None = None) -> list[Path]:
    """
    @brief Find the test programs under some paths.

    @param paths files and directories
    @param bad True for only the programs in a `bad` directory, False for only the others, None for both
    @return the programs, sorted
    """
    files = []
    for p in paths:
        path = Path(p)
        found = sorted(path.rglob("*.py")) if path.is_dir() else [path]
        for f in found:
            in_bad = "bad" in f.parts
            if bad is None or in_bad == bad:
                files.append(f)
    return files


def summary(results: list[bool], label: str) -> int:
    """
    @brief Print the number of tests that passed.

    @param results one entry per test, True if it passed
    @param label what was counted, such as "tests"
    @return the exit code: 0 if every test passed, else 1
    """
    passed = sum(results)
    print(f"\n{passed}/{len(results)} {label} passed")
    return 0 if passed == len(results) else 1
