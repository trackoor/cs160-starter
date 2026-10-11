# All seven comparison operators. Arithmetic binds more tightly, and a
# parenthesized comparison can be an operand of another comparison.
a: int = 1
b: int = 2
t: bool = False
xs: [int] = None
s: str = "s"

t = a == b
t = a != b
t = a < b
t = a <= b
t = a > b
t = a >= b
t = xs is None
t = a + 1 < b * 2
t = a - b // 2 >= -b % 3
t = (a < b) == t
t = t != (a > b)
t = (a == b) == (b == a)
t = s == "s"
t = s + "t" != "st"
t = [1] is xs
