# ===----------------------------------------------------------------------=== #
#
#                         CS160 ChocoPy Compiler
#
# lexer.py
#
# Identification: compiler/lexer.py
#
# Copyright (c) 2026, CS160 Course Staff, UC Santa Barbara
#
# ===----------------------------------------------------------------------=== #
"""The lexer turns the text of a ChocoPy program into tokens."""

from dataclasses import dataclass

from .errors import CompileError  # noqa: F401

# Use this fixed set of reserved words; every other identifier is a NAME.
KEYWORDS = {
    "False", "None", "True", "and", "as", "assert", "async", "await", "break", "class",
    "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global",
    "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise",
    "return", "try", "while", "with", "yield",
}  # fmt: skip


@dataclass
class Token:
    """
    A token: its kind, its value, and where it starts.

    `kind` is NAME, INTEGER, STRING, NEWLINE, INDENT, DEDENT or EOF, or the
    keyword or operator itself, such as 'if', 'True', '<=' or '->'. `value` is
    the identifier, the integer, or the string's characters after escapes are
    applied, and None for every other kind. `line` counts from 1 and `col`
    from 0, like `col_offset` in Python's ast.
    """

    kind: str
    value: object
    line: int
    col: int

    def __str__(self):
        shown = f" {self.value!r}" if self.value is not None else ""
        return f"{self.line}:{self.col + 1} {self.kind}{shown}"


def tokenize(source: str) -> list[Token]:
    """
    TODO(PA2): Add implementation

    @brief Split a program into tokens.

    At each position, take the longest legal token: `classic` is one NAME
    and `<=` one operator. A line that is blank or holds only a comment
    produces no tokens. Every other line ends with a NEWLINE, located just
    past its last character; there is no implicit line joining inside
    parentheses or brackets.

    Keep a stack of indentation widths, starting with [0]; a tab advances to
    the next multiple of 8. For each nonblank, non-comment line, compare its
    indentation with the stack's top. For an increase, push the width and
    emit INDENT. For a decrease, pop widths and emit a DEDENT for each until
    the width matches; if it matches no entry, report an indentation error.

    Emit NEWLINE for each code line even without a final line break. Blank
    and comment-only lines never produce NEWLINE. At the end of the input,
    emit a DEDENT for each remaining width above 0, then EOF. Final DEDENTs
    and EOF are at column 0 of the line after the last; an empty input has
    EOF at line 1, column 0. A tab counts as one character in column numbers.

    Report a lexical error with `raise CompileError(line, col + 1, message)`,
    located at the offending character, at the first digit of a bad integer
    literal, or at the opening quote of a bad string literal.

    @param source the text of the program
    @return the tokens, ending with EOF
    """
    raise NotImplementedError("tokenize is not implemented.")
