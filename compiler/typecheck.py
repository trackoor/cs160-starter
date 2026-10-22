# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# typecheck.py
#
# Identification: compiler/typecheck.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""The type checker enforces ChocoPy's scope and type rules before code generation."""

import ast

from .errors import CompileError, error_at  # noqa: F401


def check(tree: ast.Module) -> None:
    """
    TODO(PA3): Add implementation

    @brief Check a whole program before it is compiled.

    Build the symbol tables in two passes: first the global scope (every
    global variable and every function signature), then each function body
    in a scope holding its parameters, its locals and its `global` names.
    Resolve every name to its declaration, apply the type rules to every
    expression and statement, and check that a function declared to return
    `int` or `bool` returns a value on every path (`str` is added in PA4).

    If the program has errors, raise the one that comes first in the file
    (smallest line, then column), located as the writeup's table says, with
    `raise error_at(node, message)`. Keep checking after an error, but give an
    expression whose type you could not decide a special error type that no
    rule complains about again, so that one mistake does not produce a
    cascade.

    Record each expression's type on its node, for example
    `node.cp_type = "int"`, if your code generator wants to read it.

    Until you implement it, the checker accepts every program, so your PA1
    code generator keeps working.

    @param tree the program
    """
    # TODO(student): Suggested PA3 types: 'int', 'bool', and '<None>' for calls
    # without a return value. PA4 adds 'str', ('list', T), and '<Empty>' for [].
    return None
