# Unary minus binds more tightly than * // % but more loosely than indexing and
# calls: -2 * 3 is (-2) * 3, and -xs[0] is -(xs[0]).
x: int = 5
xs: [int] = None

def f(n: int) -> int:
    return -n

xs = [-1, - 2, -x]
x = -2 * 3
x = -(2 * 3)
x = 2 * -3
x = -x - -x
x = - -x
x = --x
x = -xs[0] * -xs[1]
x = -f(x) // -2
x = -f(-x) % -(x + 1)
x = 1 - -1
x = -x + 2 * -x
