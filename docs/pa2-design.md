# PA2 Design Document

<!--
Submit this document, your PA2 Claude Code or Codex sessions, or both.
AI use is optional. Staff grade the document and sessions independently
and use the higher score: Excellent (20), Good (15), Fair (10) or Poor (5).

Write the document without AI; an AI-written document receives 0. Aim for
about one page using the headings below. Explain your decisions and how you
checked them. Submit it with your code using `oneworld assessment submit`
from your PA2 folder. See Section 8 of the handout for the full rubric.
-->

**Name:**

**Perm Number / Email:**

## Lexer

Briefly describe how your lexer finds the longest token at each position, how
it reads integer and string literals, and where it reports a lexical error.

## Indentation

Describe how you produce NEWLINE, INDENT and DEDENT: the indentation stack,
blank and comment-only lines, tabs, and the end of the input.

## Parser

Describe how your parser handles precedence and associativity, groups each
`and` or `or` chain into one `BoolOp`, and rejects chained comparisons.

## Positions and Errors

Describe how statements, expressions and function parameters get their start
positions, especially with parentheses. Explain how you choose the token at
which to report a syntax error. End positions are not checked.

## Testing

For each of your three tests, explain the expected tokens, tree or error
position, the implementation mistake it catches, and how you verified this.
Describe any additional checks you ran.

The three tests cover indentation, expression-tree shape, and a lexical or
syntax error. Put them in `test/mine/pa2/`, with any rejection test in the
`bad/` subdirectory and a `# error: line:col` comment. The programs must be
original, but may test rules already covered by public tests. Parser tests
check syntax; they need not execute successfully.
