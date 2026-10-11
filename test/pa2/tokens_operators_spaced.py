# Every operator and delimiter of the subset, separated by spaces:
# + - * // % < > <= >= == != = ( ) [ ] , : ->
a: int = 17
b: int = 5
c: bool = False
xs: [int] = None

def pick(i: int, j: int) -> int:
    return i

xs = [a, b, 3]
a = a + b
a = a - b
a = a * b
a = a // b
a = a % b
c = a < b
c = a > b
c = a <= b
c = a >= b
c = a == b
c = a != b
c = xs is None
xs[0] = pick(xs[1], - b)
a = ( a )
