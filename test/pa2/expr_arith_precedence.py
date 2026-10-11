# * // % bind more tightly than + and -, and all five are left-associative:
# 8 - 3 - 1 is (8 - 3) - 1.
a: int = 8
b: int = 3
c: int = 1
d: int = 2
x: int = 0

x = 1 + 2 * 3
x = 1 * 2 + 3
x = 8 - 3 - 1
x = 8 - (3 - 1)
x = a // b % c
x = a % b // c
x = a * b // c % d
x = a - b + c - d
x = a + b * c - d // a % b
x = (a + b) * (c - d)
x = a * (b + c) // d
x = 2 * (3 + 4) - 5
x = 100 // 7 // 2
x = 100 % 7 % 2
x = a - (b - (c - d))
