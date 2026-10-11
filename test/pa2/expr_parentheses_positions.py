# Parentheses belong to the enclosing expression: in (a + b) * 3 the product
# starts at the '(' (column 0) but the sum starts after it (column 1). The same
# holds for expression statements, operands, arguments and targets.
a: int = 1
b: int = 2
t: bool = True
xs: [int] = None

xs = [(a), (b)]
(a)
((a + b))
(a + b) * 3
a * (b + 3)
((a)) + ((b))
(t) and (t)
(a) < (b)
(a) if (t) else (b)
(-a)
-(a)
(not t) == t
(xs)[0]
(len(xs))
print((a))
a = (a)
xs[(0)] = (b)
