# Expressions that use every precedence level at once, from the loosest to the
# tightest: if-else, or, and, not, comparisons, + -, * // %, unary -, then
# indexing and calls.
a: int = 1
b: bool = True
c: bool = False
xs: [int] = None
r: int = 0

def f(n: int) -> [int]:
    return [n, n + 1]

xs = [1, 2, 3]
r = a if b or c and not a == a + a * -xs[0] else f(a)[1]
r = f(-a * a + a)[0] if not (b or c) and a != a else a
b = not a < a - -a or c and b
b = (b or c) and (not b)
r = ((a if b else a) + a) * a
