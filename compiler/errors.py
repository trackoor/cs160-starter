# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# errors.py
#
# Identification: compiler/errors.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""Compile-time errors, reported as `line:col: message` with the column counted from 1."""


class CompileError(Exception):
    """CompileError is an error in the program being compiled, located at a line and column."""

    def __init__(self, line: int, col: int, message: str):
        """
        @brief Make an error.

        @param line the line, counting from 1
        @param col the column, counting from 1
        @param message what is wrong
        """
        super().__init__(f"{line}:{col}: {message}")
        self.line = line
        self.col = col
        self.message = message


def error_at(node, message: str) -> CompileError:
    """
    @brief Make an error located where an AST node starts.

    @param node the node; its `lineno` and `col_offset` give the position
    @param message what is wrong
    @return the error, to raise
    """
    return CompileError(node.lineno, node.col_offset + 1, message)
