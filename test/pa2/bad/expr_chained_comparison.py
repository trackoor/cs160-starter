# error: 4:13
# comparisons do not chain: after 1 < x, a second < cannot continue the expression
x: int = 2
print(1 < x < 3)
