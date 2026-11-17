# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# local_opt.py
#
# Identification: compiler/local_opt.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""Local optimization simplifies each block of a function in SSA form."""

from .ir import Function, Instr  # noqa: F401


def optimize(fn: Function) -> None:
    """
    TODO(PA5): Add implementation

    @brief Simplify each block of a function in SSA form, in place.

    1. Fold constants with LLVM's semantics: `i32` arithmetic wraps around,
       and `sdiv` and `srem` truncate toward zero. Never fold a division by
       zero.
    2. Apply the identities x + 0 = x and x * 1 = x.
    3. Number the pure instructions of each block, so that a computation
       repeated in the same block reuses the earlier result. Never merge two
       calls, and merge two loads only if no store or call between them can
       have changed memory.

    Until you implement it, this pass changes nothing.

    @param fn the function, in SSA form
    """
    return None
