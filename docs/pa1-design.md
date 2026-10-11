# PA1 Design Document

<!--
Submit this document, your PA1 Claude Code or Codex sessions, or both.
Staff grade the document and sessions independently and use the higher
score. See Section 8 of the PA1 handout.

Write the document without AI; an AI-written document receives 0. Aim for
about one page. Submit it with your code using `oneworld assessment submit`.
Explain your design decisions and how you checked them.
-->

**Name:**

**Perm Number / Email:**

## Values and Variables

Describe how your code generator represents an `int` and a `bool`, where each
variable lives, and how an expression hands its value to the code that uses it.

## Floor Division and Modulo

Describe how you compute `//` and `%` with Python's rounding from LLVM's
`sdiv` and `srem`, and how the program stops on a zero divisor. Which case
needed the correction, and how did you convince yourself it is right?

## Control Flow

Describe the blocks and branches you emit for `if`/`elif`/`else` and `while`,
and how `and`, `or` and conditional expressions evaluate only the operands
they need.

## Testing

For each of your three tests in `test/mine/pa1`, say what it checks, what
it prints, and which wrong compiler it would catch. Say how else you checked
your work.
