xs: [int] = None
x: int = 0
i: int = 0
xs = [1, 2, 3, 4, 5]
for x in xs:
    if i + 1 < len(xs):
        xs[i + 1] = xs[i + 1] + x
    print(x)
    i = i + 1
print(xs[4])
i = 0
for x in xs:
    if i > 0:
        xs[i - 1] = 0
    i = i + 1
print(xs[0] + xs[1] + xs[2] + xs[3] + xs[4])
i = 0
for x in xs:
    xs[len(xs) - 1 - i] = i
    print(x)
    i = i + 1
