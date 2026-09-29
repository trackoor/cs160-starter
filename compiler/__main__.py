# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# __main__.py
#
# Identification: compiler/__main__.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""The compiler's command-line driver.

    python3 -m compiler run   prog.py      compile with clang and run
    python3 -m compiler ll    prog.py      print the LLVM IR
    python3 -m compiler build prog.py -o prog
    python3 -m compiler tokens prog.py     print your lexer's tokens (PA2)
    python3 -m compiler ast   prog.py      print ast.dump of your parser's tree (PA2)
    python3 -m compiler ast --positions prog.py    print where each statement and expression starts
    python3 -m compiler check prog.py      type-check only (PA3)
    python3 -m compiler opt -O1 prog.ll    run your passes on an existing .ll file (PA5, PA6)
    python3 -m compiler opt --passes=global prog.ll    run only the named passes

Options:
    --parser=python    read the program with Python's ast.parse
    --parser=ours      read it with your PA2 lexer and parser (the default from PA2 on)
    -O1                after code generation, build SSA and optimize locally (PA5)
    -O2                also optimize globally (PA6)
    --verify           check that the IR is well formed (after every pass, from PA5 on)
"""

import argparse
import ast
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

from . import config
from .errors import CompileError

ROOT = Path(__file__).resolve().parent.parent
RUNTIME = ROOT / "runtime" / "runtime.c"


class DriverError(Exception):
    """DriverError is a failure with no source position: an unknown pass, IR that fails --verify, or clang."""


def read_program(source: str, parser: str) -> ast.Module:
    """
    @brief Parse a program with the chosen parser.

    @param source the text of the program
    @param parser "python" for Python's ast.parse, "ours" for your PA2 parser
    @return the module
    """
    if parser == "python":
        try:
            return ast.parse(source)
        except SyntaxError as e:
            raise CompileError(e.lineno or 1, e.offset or 1, e.msg)
    from .parser import parse

    return complete(parse(source))


def complete(tree: ast.AST) -> ast.AST:
    """
    @brief Fill in the fields a parser may leave out, as Python 3.13 and later do when a node is built.

    A list field becomes [], an optional field None, and a missing ctx Load(). Older
    Pythons leave such fields missing, and the tree would then compare equal to
    ast.parse's on some Pythons but not on others.

    @param tree a tree from your parser
    @return the same tree
    """
    for node in ast.walk(tree):
        signature = re.match(r"\w+\((.*)\)", type(node).__doc__ or "")
        for kind, mark, name in re.findall(r"(\w+)([*?]?) (\w+)", signature.group(1) if signature else ""):
            if not hasattr(node, name):
                if mark == "*":
                    setattr(node, name, [])
                elif mark == "?":
                    setattr(node, name, None)
                elif kind == "expr_context":
                    setattr(node, name, ast.Load())
    return tree


def positions(tree: ast.AST) -> str:
    """
    @brief List each statement and expression with the line:column where it starts, nested by depth.

    Columns count from 1, as in error messages; ast.dump does not show positions.

    @param tree the tree
    @return one line per statement or expression, for example "BinOp 2:7"
    """
    lines = []

    def show(node: ast.AST, depth: int) -> None:
        if isinstance(node, (ast.stmt, ast.expr)):
            line, col = getattr(node, "lineno", None), getattr(node, "col_offset", None)
            where = f"{line}:{col + 1}" if line is not None and col is not None else "no position"
            lines.append("  " * depth + f"{type(node).__name__} {where}")
            depth += 1
        for child in ast.iter_child_nodes(node):
            show(child, depth)

    show(tree, 0)
    return "\n".join(lines)


def dump(tree: ast.AST, indent: int | None = None) -> str:
    """
    @brief Print a tree as ast.dump does on Python 3.12, whatever Python runs this.

    Python 3.13 and later leave out empty lists and None unless asked.

    @param tree the tree
    @param indent as for ast.dump
    @return the text
    """
    return ast.dump(tree, indent=indent, **({"show_empty": True} if sys.version_info >= (3, 13) else {}))


def front_end(source: str, parser: str) -> ast.Module:
    """
    @brief Parse a program, check that it is inside the released part of ChocoPy, and, from PA3 on, type-check it.

    @param source the text of the program
    @param parser "python" or "ours"
    @return the checked module
    """
    from .subset import check_subset

    tree = read_program(source, parser)
    check_subset(tree, config.RELEASED)
    if config.RELEASED >= 3:
        from .typecheck import check

        check(tree)
    return tree


def optimize(ir_text: str, level: int, verify: bool, only: list[str] | None = None) -> str:
    """
    @brief Run your optimization passes on the IR of a module.

    -O1 runs `ssa.construct` and `local_opt.optimize` on each function; -O2
    adds `global_opt.optimize`. Blocks that cannot be reached from the entry
    block are removed first.

    @param ir_text the IR, as your code generator or the reference compiler prints it
    @param level 0, 1 or 2
    @param verify whether to check the IR after every pass with `Function.verify`
    @param only the passes to run instead, by name: "ssa", "local", "global"
    @return the optimized IR
    """
    from . import ir

    module = ir.parse(ir_text)
    names = only if only is not None else (["ssa", "local"] if level >= 1 else []) + (["global"] if level >= 2 else [])
    passes = []
    for name in names:
        if name == "ssa":
            from .ssa import construct

            passes.append(("ssa", construct))
        elif name == "local":
            from .local_opt import optimize as local

            passes.append(("local", local))
        elif name == "global":
            from .global_opt import optimize as global_

            passes.append(("global", global_))
        else:
            raise DriverError(f"unknown pass {name!r}; the passes are ssa, local and global")
    for function in module.functions:
        function.remove_unreachable_blocks()
        for name, run_pass in passes:
            run_pass(function)
            if verify:
                problems = function.verify()
                if problems:
                    raise DriverError(f"after the {name} pass, @{function.name}: {problems[0]}")
    return module.render()


def compile_to_ir(path: str, parser: str, level: int, verify: bool) -> str:
    """
    @brief Compile a program file to LLVM IR.

    @param path the program file
    @param parser "python" or "ours"
    @param level the optimization level, 0 to 2
    @param verify whether to check the IR with `Function.verify`
    @return the IR
    """
    source = Path(path).read_text()
    tree = front_end(source, parser)
    from .codegen import generate

    text = generate(tree)
    if level > 0:
        text = optimize(text, level, verify)
    elif verify:
        from . import ir

        try:
            functions = ir.parse(text).functions
        except ir.IRError as e:
            raise DriverError(f"cannot read the IR: {e}")
        for function in functions:
            problems = function.verify()
            if problems:
                raise DriverError(f"@{function.name}: {problems[0]}")
    return text


def clang() -> str:
    """
    @brief Find the C compiler: $CC if it is set, else clang on the PATH.

    @return its path
    """
    found = os.environ.get("CC") or shutil.which("clang")
    if not found:
        sys.exit("clang was not found; see Setup in README.md, or run python3 tools/doctor.py")
    return found


def build(ir_text: str, output: str) -> None:
    """
    @brief Compile IR with clang, together with the runtime, into an executable.

    clang runs with -O0, so the only optimizations are your own passes.

    @param ir_text the IR
    @param output the executable's path
    """
    with tempfile.TemporaryDirectory() as tmp:
        ll = Path(tmp) / "prog.ll"
        ll.write_text(ir_text)
        result = subprocess.run(
            [clang(), "-O0", "-w", "-Wno-override-module", "-o", output, str(ll), str(RUNTIME)],
            capture_output=True,
            text=True,
        )
    if result.returncode:
        # clang names the temporary file; "IR line 18:32" points into `python3 -m compiler ll` instead.
        sys.stderr.write(result.stderr.replace(str(ll) + ":", "IR line "))
        raise DriverError("clang rejected the generated IR (see the messages above)")


def not_released(args) -> str | None:
    """
    @brief Tell whether a command needs an assignment that has not been released yet.

    @param args the parsed command line
    @return why the command cannot run yet, or None if it can
    """
    released = config.RELEASED
    if released < 2 and (args.command == "tokens" or args.parser == "ours"):
        return "your own lexer and parser arrive in PA2; until then programs are read with ast.parse"
    if released < 5 and (args.command == "opt" or args.level > 0):
        return "optimization (-O1 and the opt command) arrives in PA5"
    if released < 6 and (args.level == 2 or "global" in (args.passes or "")):
        return "global optimization (-O2) arrives in PA6"
    return None


def main(argv=None) -> int:
    """
    @brief Run the command line; see the module's description.

    @param argv the arguments, or None for sys.argv
    @return the exit code: the program's own for `run`, else 0 on success and 1 on an error
    """
    ap = argparse.ArgumentParser(
        prog="python3 -m compiler", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("command", choices=["run", "ll", "build", "tokens", "ast", "check", "opt"])
    ap.add_argument("file")
    ap.add_argument("--parser", choices=["python", "ours"], default="ours" if config.RELEASED >= 2 else "python")
    ap.add_argument("-O", dest="level", type=int, choices=[0, 1, 2], default=0)
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--passes", help="opt only: run exactly these passes, e.g. --passes=global")
    ap.add_argument("-o", dest="output")
    ap.add_argument("--positions", action="store_true", help="ast only: print positions instead of ast.dump")
    args = ap.parse_args(argv)
    reason = not_released(args)
    if reason:
        print(f"python3 -m compiler: {reason}", file=sys.stderr)
        return 1

    try:
        if args.command == "tokens":
            from .lexer import tokenize

            for token in tokenize(Path(args.file).read_text()):
                print(token)
            return 0
        if args.command == "ast":
            tree = read_program(Path(args.file).read_text(), args.parser)
            print(positions(tree) if args.positions else dump(tree, indent=2))
            return 0
        if args.command == "check":
            front_end(Path(args.file).read_text(), args.parser)
            return 0
        if args.command == "opt":
            only = args.passes.split(",") if args.passes else None
            print(optimize(Path(args.file).read_text(), args.level, args.verify, only), end="")
            return 0
        text = compile_to_ir(args.file, args.parser, args.level, args.verify)
        if args.command == "ll":
            print(text, end="")
            return 0
        if args.command == "build":
            build(text, args.output or Path(args.file).with_suffix("").name)
            return 0
        with tempfile.TemporaryDirectory() as tmp:
            exe = str(Path(tmp) / "prog")
            build(text, exe)
            sys.stdout.flush()
            code = subprocess.run([exe]).returncode
            if code < 0:  # killed by a signal: report it, and exit as a shell would (139 for SIGSEGV)
                name = signal.Signals(-code).name if -code in signal.valid_signals() else f"signal {-code}"
                print(f"{args.file}: the program crashed with {name}", file=sys.stderr)
                return 128 - code
            return code
    except CompileError as e:
        print(f"{args.file}:{e}", file=sys.stderr)
        return 1
    except DriverError as e:
        print(f"{args.file}: {e}", file=sys.stderr)
        return 1
    except NotImplementedError as e:
        print(f"{args.file}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
