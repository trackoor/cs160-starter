# ast.parse flattens a chain of the same boolean operator into one BoolOp
# (a and b and c has three values), but a parenthesized chain stays a nested
# BoolOp, and a mix of and/or nests by precedence.
a: bool = True
b: bool = False
c: bool = True
d: bool = False
r: bool = False

r = a and b
r = a and b and c
r = a and b and c and d
r = a or b or c or d
r = a and (b and c)
r = (a and b) and c
r = (a and b) and (c and d)
r = a or (b or c) or d
r = a and b or c and d
r = a or b and c or d
r = (a or b) and (c or d)
r = a and b and (c or d) and a
r = a or b and c and d
r = ((a and b)) and c
r = (a and b or c) and d
