# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# ssa.py
#
# Identification: compiler/ssa.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""SSA construction promotes stack slots to SSA values, as LLVM's mem2reg does."""

from .ir import Function, Instr  # noqa: F401


def immediate_dominators(fn: Function) -> dict[str, str]:
    """
    TODO(PA5): Add implementation

    @brief Find the immediate dominator of every block.

    Block A dominates block B when every path from the entry block to B goes
    through A. The immediate dominator of B is the block closest to B, other
    than B itself, that dominates B. Compute it yourself; `fn.dominators()`
    is there only to check your results.

    @param fn the function
    @return the label of each block -> the label of its immediate dominator;
        `entry` maps to itself
    """
    raise NotImplementedError("immediate_dominators is not implemented.")


def dominance_frontiers(fn: Function, idom: dict[str, str]) -> dict[str, set[str]]:
    """
    TODO(PA5): Add implementation

    @brief Find the dominance frontier of every block.

    The dominance frontier of block A holds each block B that A does not
    strictly dominate but that has a predecessor A dominates: the blocks
    where A's dominance ends.

    @param fn the function
    @param idom the immediate dominators, from `immediate_dominators`
    @return the label of each block -> the labels of its dominance frontier
    """
    raise NotImplementedError("dominance_frontiers is not implemented.")


def construct(fn: Function) -> None:
    """
    TODO(PA5): Add implementation

    @brief Rewrite a function into SSA form, in place.

    1. Compute the dominators and the dominance frontier of every block.
    2. Find the promotable slots: the `alloca`s in the entry block whose only
       uses are loads from and stores to the whole slot.
    3. For each promotable slot, place a phi at the iterated dominance
       frontier of the blocks that store to it.
    4. Walk the dominator tree from the entry block with one stack of current
       values per slot, starting each stack with `undef`. A store pushes its
       value, a load is replaced by the value on top, and a phi you placed
       pushes itself. Before leaving a block, fill in the phi operands of its
       successors; after visiting its children, pop what it pushed.
    5. Delete the promoted `alloca`s and their loads and stores.

    The driver has already removed the blocks that cannot be reached from the
    entry block. Until you implement it, this pass changes nothing.

    @param fn the function, as `ir.parse` reads it
    """
    return None
