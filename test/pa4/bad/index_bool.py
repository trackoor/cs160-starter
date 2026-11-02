# error: 5:10
# An index must be an int, not a bool.
xs: [int] = None
xs = [1, 2]
print(xs[True])
