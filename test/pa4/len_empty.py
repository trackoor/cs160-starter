# len([]) is allowed: len accepts a str, any list, and [].
n: int = 0
xs: [int] = None
n = len([])
print(n)
xs = []
print(len(xs))
xs = xs + [1, 2]
print(len(xs))
