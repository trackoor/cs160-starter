# The conditional expression binds most loosely and is right-associative:
# a if t else b if u else 0 is a if t else (b if u else 0). Its test is parsed
# at the level of or.
a: int = 1
b: int = 2
t: bool = True
u: bool = False
x: int = 0
xs: [int] = None

x = a if t else b
x = a if t else b if u else 0
x = (a if t else b) if u else 0
x = a if (t if u else t) else b
x = a if t else (b if u else 0)
x = a if t or u else b
x = a if t and not u else b
t = t or u if u and t else u or t
x = a + 1 if a < b else b * 2
xs = [a if t else b, b if u else a]
print(a if t else b)
x = xs[0 if t else 1]
x = -a if t else -b
