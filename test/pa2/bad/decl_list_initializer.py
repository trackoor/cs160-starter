# error: 3:13
# [] is an expression, not a literal, so it cannot initialize a variable (use None)
xs: [int] = []
xs = [1]
print(xs[0])
