# Calls and indexing are postfix operators that chain left to right; every node
# in a chain such as f(x)[0][1] starts at the column of its leftmost token.
xss: [[int]] = None
xs: [int] = None
s: str = "abc"
x: int = 0

def f(n: int) -> [[int]]:
    return [[n, n + 1], [n + 2]]

def g(n: int) -> int:
    return n

x = f(x)[0][1]
x = f(g(g(x)))[1][0]
xss = f(1)
xs = xss[0]
x = xss[0][1]
x = xss[g(0)][g(1)]
x = xs[xs[0] + 1]
x = [1, 2, 3][0]
x = [[4], [5]][1][0]
s = "abc"[1]
s = s[0][0]
x = (xs)[0]
x = (f(2))[1][0]
x = len(f(x)[0])
