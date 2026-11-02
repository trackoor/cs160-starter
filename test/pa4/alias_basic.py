xs: [int] = None
ys: [int] = None
zs: [int] = None
x: int = 5
xs = [1, 2, 3]
ys = xs
ys[0] = 7
print(xs[0])
xs[2] = ys[0] + ys[1]
print(ys[2])
print(xs is ys)
zs = [7, 2, 9]
print(zs is xs)
print(zs[2] == xs[2])
ys = [4, 5, 6]
ys[1] = 50
print(xs[1])
print(ys[1])
print(xs is ys)
zs = [x, x]
x = 6
print(zs[0])
zs[1] = x
print(zs[1])
xs = zs
zs = None
print(xs[0] + xs[1])
print(zs is None)
