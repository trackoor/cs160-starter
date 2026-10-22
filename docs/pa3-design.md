# PA3 Design Document

<!--
Hand in this document, your AI sessions, or both (Section "Submitting your
work" of the PA3 writeup). Staff grade each one on its own and keep the
higher grade: Excellent, Good, Fair or Poor.

Write it yourself: a design document written with AI earns no points. About
one page (250-900 words). It is handed in with your code when you run
`oneworld assessment submit`, and graded on how well it explains your design
decisions and how you checked them.
-->

**Name:**

**Perm Number / Email:**

## Scopes

Describe your symbol tables: how you collect the global scope, how a function
body sees its parameters, locals and `global` names, and how you decide
whether code may assign to a name.

## Type Rules

Describe how you apply the type rules, how you report the earliest error in
the file, and how you keep one mistake from causing more. Say how you check
that a function returns a value on every path.

## Functions in LLVM

Describe how you compile a function: its signature, the slots of its
parameters, global variables, calls, and the names you give to functions and
globals.

## Testing

For each of your three tests in `test/mine/pa3`, say what it checks, what
it prints (or where it must be rejected), and which wrong compiler it would
catch. Say how else you checked your work.

The three tests cover lexical scope, a type error with its expected position,
and arguments passed in the wrong positions. They may cover behavior that
public tests also check, but the programs must be your own.
