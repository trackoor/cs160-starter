# not binds more loosely than comparisons (not a == b is not (a == b)) and more
# tightly than and/or; after a comparison operator, not needs parentheses.
a: int = 1
b: int = 2
t: bool = True
xs: [int] = None

t = not a == b
t = not not t
t = not a < b and t
t = not (a < b and t)
t = t and not t
t = t or not t and t
t = True == (not False)
t = (not t) == t
t = not xs is None
t = not -a > b
t = not a + 1 != b * 2
