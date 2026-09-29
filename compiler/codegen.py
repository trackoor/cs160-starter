# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# codegen.py
#
# Identification: compiler/codegen.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""CodeGen translates a checked ChocoPy program into an LLVM module."""

import ast

from .emit import Function, Module


class CodeGen:
    """
    CodeGen emits the LLVM IR of one program. Every variable lives in memory
    reserved for it, and `expr` returns the value of each expression.
    """

    def __init__(self):
        self.module = Module()
        self.fn = Function("define i32 @main()")
        # TODO(student): You can modify or remove these member variables as you like.
        # ChocoPy variable name -> (slot, ChocoPy type), e.g. "x" -> ("%x.addr", "int")
        self.variables: dict[str, tuple[str, str]] = {}

    def program(self, tree: ast.Module) -> str:
        """
        @brief Emit a whole program: its declarations, then its statements, as `@main`.

        @param tree the program, already checked to be inside the released part of ChocoPy
        @return the text of the LLVM module
        """
        for node in tree.body:
            if isinstance(node, ast.AnnAssign):
                self.declaration(node)
            else:
                self.statement(node)
        self.module.add_function(self.fn.render("ret i32 0"))
        return self.module.render()

    def declaration(self, node: ast.AnnAssign) -> None:
        """
        TODO(PA1): Add implementation

        @brief Declare a variable, such as `x: int = 5` or `done: bool = False`.

        Reserve the variable's slot with `self.fn.slot(name, llvm_type)`, which
        places the `alloca` in the entry block and returns `%name.addr`, and
        store the initial value in it. An `int` is an `i32` and a `bool` is an
        `i1`, with the constants `true` and `false`.

        @param node the declaration
        """
        raise NotImplementedError("CodeGen.declaration is not implemented.")

    def statement(self, node: ast.stmt) -> None:
        """
        TODO(PA1): Add implementation

        @brief Emit the instructions of one statement.

        The starter handles expression statements and `pass`. Add assignment,
        `if`/`elif`/`else` and `while`. Take fresh labels with, for example,
        `self.fn.labels("while.cond", "while.body", "while.end")`, and start a
        block with `self.fn.label(name)`; if the current block has no
        terminator yet, the emitter first adds a branch to the new block.

        @param node the statement
        """
        if isinstance(node, ast.Expr):
            self.expr(node.value)
        elif isinstance(node, ast.Pass):
            pass
        else:
            raise NotImplementedError(f"CodeGen.statement is not implemented for {type(node).__name__}.")

    def expr(self, node: ast.expr) -> tuple[str, str]:
        """
        TODO(PA1): Add implementation

        @brief Emit the instructions that compute an expression.

        The starter handles integer literals and `print` of an `int`. Add
        `True` and `False`, variables, unary `-` and `not`, `+`, `-`, `*`,
        `//`, `%`, the comparisons, `and`, `or`, and conditional expressions.

        1. `//` rounds toward negative infinity and `%` takes the sign of the
           divisor, as in Python, while LLVM's `sdiv` and `srem` truncate.
           A zero divisor calls `cp_error_div()`.
        2. `and`, `or` and conditional expressions evaluate only the parts
           that decide their value.
        3. `cp_print_int(i32)` and `cp_print_bool(i32)` print a value and a
           newline; widen an `i1` to `i32` with `zext` first.

        Take a new name for each result with `self.fn.temp()`, and add a line
        of IR with `self.fn.emit(text)`.

        @param node the expression
        @return (value, type): the value as IR writes it, such as `5`, `true`
        or `%t3`, and its ChocoPy type, such as `int`
        """
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return str(node.value), "int"
        if isinstance(node, ast.Call) and node.func.id == "print":
            value, t = self.expr(node.args[0])
            if t == "int":
                self.fn.emit(f"call void @cp_print_int(i32 {value})")
                return "", "<None>"
        raise NotImplementedError(f"CodeGen.expr is not implemented for {type(node).__name__}.")


def generate(tree: ast.Module) -> str:
    """
    @brief Compile a checked program to LLVM IR. The driver calls this function.

    @param tree the program
    @return the text of the LLVM module
    """
    return CodeGen().program(tree)
