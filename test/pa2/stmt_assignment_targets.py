# Assignment targets: a variable, a list element, an element of an element, and
# an index into any expression (a call, or a parenthesized name). The target has
# ctx=Store(); only the outermost index expression is stored to.
x: int = 0
xs: [int] = None
xss: [[int]] = None

def row(i: int) -> [int]:
    return xss[i]

xs = [1, 2, 3]
xss = [xs, [4, 5]]
x = 1
xs[0] = x
xs[x] = xs[x - 1] + 1
xss[1][0] = 9
xss[x][x - 1] = xss[0][0]
row(0)[1] = 7
(xs)[2] = 8
x = x
