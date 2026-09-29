# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# subset.py
#
# Identification: compiler/subset.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""The subset check rejects programs outside the course's ChocoPy subset.

`ast.parse` accepts all of Python, so when the driver reads a program with it,
this check keeps out everything the subset does not have (classes, `x = y = 1`,
chained comparisons, ...) and everything not yet released: functions arrive in
PA3, and lists, strings and `None` in PA4. Your own PA2 parser enforces the
syntax itself; this check still runs afterwards.
"""

import ast

from .errors import error_at

MAX_INT = 2**31 - 1


class SubsetChecker:
    """SubsetChecker walks a program and raises a CompileError at the first construct outside the subset."""

    def __init__(self, level: int):
        """
        @brief Make a checker for the part of ChocoPy released so far.

        @param level the number of assignments released
        """
        self.functions_allowed = level >= 3
        self.heap_allowed = level >= 4

    def fail(self, node, message):
        raise error_at(node, message)

    def need_functions(self, node, what):
        if not self.functions_allowed:
            self.fail(node, f"{what} arrive in PA3")

    def need_heap(self, node, what):
        if not self.heap_allowed:
            self.fail(node, f"{what} arrive in PA4")

    # Programs and declarations -------------------------------------------------

    def program(self, tree: ast.Module):
        seen_statement = False
        for node in tree.body:
            if self.is_declaration(node):
                if seen_statement:
                    self.fail(node, "declarations must come before the first statement")
                self.declaration(node, top_level=True)
            else:
                seen_statement = True
                self.statement(node, in_function=False)

    def is_declaration(self, node) -> bool:
        return isinstance(node, (ast.AnnAssign, ast.FunctionDef, ast.Global, ast.Nonlocal))

    def declaration(self, node, top_level):
        if isinstance(node, ast.AnnAssign):
            if not isinstance(node.target, ast.Name) or not node.simple:
                self.fail(node, "a declaration names one variable, as in x: int = 0")
            if node.value is None:
                self.fail(node, "a declaration needs an initial value")
            self.type_annotation(node.annotation)
            self.literal(node.value)
        elif isinstance(node, ast.FunctionDef):
            self.need_functions(node, "functions")
            if not top_level:
                self.fail(node, "nested functions are not in the course subset")
            self.function(node)
        elif isinstance(node, ast.Global):
            if top_level:
                self.fail(node, "global declarations belong inside a function")
            self.need_functions(node, "global declarations")
            if len(node.names) != 1:
                self.fail(node, "declare one global name per line")
        else:
            self.fail(node, "nonlocal is not in the course subset")

    def function(self, node: ast.FunctionDef):
        args = node.args
        if (
            node.decorator_list
            or args.posonlyargs
            or args.vararg
            or args.kwonlyargs
            or args.kwarg
            or args.defaults
            or args.kw_defaults
            or getattr(node, "type_params", None)
        ):
            self.fail(node, "functions take only plain, annotated parameters")
        for arg in args.args:
            if arg.annotation is None:
                self.fail(arg, "every parameter needs a type annotation")
            self.type_annotation(arg.annotation)
        if node.returns is not None:
            self.type_annotation(node.returns)
        seen_statement = False
        for stmt in node.body:
            if isinstance(stmt, (ast.AnnAssign, ast.Global, ast.Nonlocal, ast.FunctionDef)):
                if seen_statement:
                    self.fail(stmt, "declarations must come before the first statement")
                self.declaration(stmt, top_level=False)
            else:
                seen_statement = True
                self.statement(stmt, in_function=True)
        if not seen_statement:
            self.fail(node, "a function body needs at least one statement")

    def type_annotation(self, node):
        if isinstance(node, ast.Name) and node.id in ("int", "bool"):
            return
        if isinstance(node, ast.Name) and node.id == "str":
            self.need_heap(node, "strings")
            return
        if isinstance(node, ast.List) and len(node.elts) == 1:
            self.need_heap(node, "lists")
            self.type_annotation(node.elts[0])
            return
        self.fail(node, "a type is int, bool, str, or a list type such as [int]")

    def literal(self, node):
        if isinstance(node, ast.Constant):
            value = node.value
            if isinstance(value, bool):
                return
            if isinstance(value, int):
                if value > MAX_INT:
                    self.fail(node, "integer literal is larger than 2147483647")
                return
            if value is None:
                self.need_heap(node, "None values")
                return
            if isinstance(value, str):
                self.need_heap(node, "strings")
                self.string_value(node, value)
                return
        self.fail(node, "an initial value must be a literal (write x: int = 0, then assign)")

    def string_value(self, node, value):
        for ch in value:
            if not (32 <= ord(ch) <= 126 or ch in "\n\t"):
                self.fail(node, "strings may contain only printable ASCII, \\n and \\t")

    # Statements -----------------------------------------------------------------

    def statement(self, node, in_function):
        if isinstance(node, ast.Assign):
            if len(node.targets) != 1:
                self.fail(node, "assign to one target at a time")
            target = node.targets[0]
            if isinstance(target, ast.Subscript):
                self.need_heap(target, "lists")
                self.expression(target.value)
                self.expression(target.slice)
            elif not isinstance(target, ast.Name):
                self.fail(target, "you can assign to a variable or a list element")
            self.expression(node.value)
        elif isinstance(node, ast.Expr):
            self.expression(node.value)
        elif isinstance(node, ast.Pass):
            pass
        elif isinstance(node, ast.If):
            self.expression(node.test)
            self.block(node.body, in_function)
            self.block(node.orelse, in_function, allow_empty=True)
        elif isinstance(node, ast.While):
            if node.orelse:
                self.fail(node, "while ... else is not in the course subset")
            self.expression(node.test)
            self.block(node.body, in_function)
        elif isinstance(node, ast.For):
            self.need_heap(node, "for loops")
            if node.orelse or not isinstance(node.target, ast.Name):
                self.fail(node, "a for loop assigns one variable and has no else")
            self.expression(node.iter)
            self.block(node.body, in_function)
        elif isinstance(node, ast.Return):
            self.need_functions(node, "return statements")
            if not in_function:
                self.fail(node, "return outside a function")
            if node.value is not None:
                self.expression(node.value)
        elif self.is_declaration(node):
            self.fail(node, "declarations must come before the first statement")
        else:
            self.fail(node, f"{type(node).__name__} statements are not in the course subset")

    def block(self, statements, in_function, allow_empty=False):
        for stmt in statements:
            if self.is_declaration(stmt):
                self.fail(stmt, "declarations belong at the top of a program or function")
            self.statement(stmt, in_function)

    # Expressions ----------------------------------------------------------------

    def expression(self, node):
        if isinstance(node, ast.Constant):
            self.literal(node)
        elif isinstance(node, ast.Name):
            pass
        elif isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, (ast.USub, ast.Not)):
                self.fail(node, "the unary operators are - and not")
            self.expression(node.operand)
        elif isinstance(node, ast.BinOp):
            if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.FloorDiv, ast.Mod)):
                self.fail(node, "the arithmetic operators are +, -, *, // and %")
            self.expression(node.left)
            self.expression(node.right)
        elif isinstance(node, ast.BoolOp):
            for value in node.values:
                self.expression(value)
        elif isinstance(node, ast.Compare):
            if len(node.ops) != 1:
                self.fail(node, "comparisons do not chain in ChocoPy")
            op = node.ops[0]
            if isinstance(op, ast.Is):
                self.need_heap(node, "comparisons with is")
            elif not isinstance(op, (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE)):
                self.fail(node, "the comparisons are ==, !=, <, <=, >, >= and is")
            self.expression(node.left)
            self.expression(node.comparators[0])
        elif isinstance(node, ast.IfExp):
            self.expression(node.test)
            self.expression(node.body)
            self.expression(node.orelse)
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.keywords:
                self.fail(node, "a call names a function and passes positional arguments")
            if any(isinstance(arg, ast.Starred) for arg in node.args):
                self.fail(node, "a call passes positional arguments")
            name = node.func.id
            if name == "len":
                self.need_heap(node, "calls to len")
            elif name != "print":
                self.need_functions(node, "calls to your own functions")
            for arg in node.args:
                self.expression(arg)
        elif isinstance(node, ast.List):
            self.need_heap(node, "lists")
            for elt in node.elts:
                self.expression(elt)
        elif isinstance(node, ast.Subscript):
            self.need_heap(node, "indexes such as xs[0]")
            if isinstance(node.slice, ast.Slice):
                self.fail(node, "slices are not in the course subset")
            self.expression(node.value)
            self.expression(node.slice)
        else:
            self.fail(node, f"{type(node).__name__} expressions are not in the course subset")


def check_subset(tree: ast.Module, level: int) -> None:
    """
    @brief Check that a program stays inside the released part of the course's ChocoPy subset.

    @param tree the program
    @param level the number of assignments released
    """
    SubsetChecker(level).program(tree)
