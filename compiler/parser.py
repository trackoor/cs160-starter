# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# parser.py
#
# Identification: compiler/parser.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""The parser turns tokens into the `ast.Module` that `ast.parse` builds."""

import ast

from .errors import CompileError
from .lexer import Token, tokenize


def at(node, line: int, col: int):
    """
    @brief Set a node's start position.

    @param node an AST node
    @param line its line, counting from 1
    @param col its column, counting from 0
    @return the node
    """
    node.lineno = line
    node.col_offset = col
    return node


def function_def(name, params, body, returns, line, col) -> ast.FunctionDef:
    """
    @brief Build a function node with the fields required by the current Python version.

    @param name the function's name
    @param params its parameters, a list of `ast.arg` nodes
    @param body its statements
    @param returns its return annotation, or None
    @param line the line of the `def`
    @param col the column of the `def`
    @return the node
    """
    arguments = ast.arguments(posonlyargs=[], args=params, vararg=None, kwonlyargs=[],
                              kw_defaults=[], kwarg=None, defaults=[])  # fmt: skip
    fields = dict(name=name, args=arguments, body=body, decorator_list=[], returns=returns, type_comment=None)
    if "type_params" in ast.FunctionDef._fields:
        fields["type_params"] = []
    return at(ast.FunctionDef(**fields), line, col)


class Parser:
    """
    Complete program() and add methods to parse ChocoPy.

    Recursive descent and precedence climbing are useful approaches;
    the tests check the resulting tree, not which algorithm you choose.
    """

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0
        # Add fields and methods as needed.

    def peek(self, ahead: int = 0) -> Token:
        """
        @brief Look at a token without consuming it.

        @param ahead how many tokens past the current one
        @return the token, or EOF past the end
        """
        return self.tokens[min(self.i + ahead, len(self.tokens) - 1)]

    def advance(self) -> Token:
        """
        @brief Consume the current token.

        @return the token
        """
        token = self.peek()
        self.i += 1
        return token

    def expect(self, kind: str) -> Token:
        """
        @brief Consume the current token, which must be of the given kind.

        Raises a CompileError at the token if its kind differs.

        @param kind the kind the token must have
        @return the token
        """
        token = self.peek()
        if token.kind != kind:
            raise CompileError(token.line, token.col + 1, f"expected {kind!r}, found {token.kind!r}")
        return self.advance()

    def program(self) -> ast.Module:
        """
        TODO(PA2): Add implementation

        @brief Parse a whole program.

        Build the tree `ast.parse` builds for syntactically valid ChocoPy: the
        same node types and fields, and the same `lineno` and `col_offset` on
        every statement, expression and function parameter. End positions are
        not checked. Do not check types or execute the program.

        Track where each expression's source text starts, including opening
        parentheses: in `(1 + 2) * 3`, the product starts at column 0 and the
        inner sum at column 1. One approach is to return both the node and
        the source start position from each expression parsing method.

        For a syntax error, raise CompileError at the first token that cannot
        continue the program: `CompileError(token.line, token.col + 1, message)`.

        @return the module
        """
        raise NotImplementedError("Parser.program is not implemented.")


def parse(source: str) -> ast.Module:
    """
    @brief Parse a program. The driver calls this function.

    @param source the text of the program
    @return the module
    """
    return Parser(tokenize(source)).program()
