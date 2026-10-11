# error: 4:1
# a global declaration belongs at the start of a function body, not at the top level
x: int = 0
global x
x = 1
