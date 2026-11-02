xs: [int] = None
ys: [int] = None
zs: [int] = None
bs: [bool] = None

def ident(p: [int]) -> [int]:
    return p

def empty(p: [int]) -> bool:
    return p is None or len(p) == 0

print(xs is None)
print(xs is ys)
print(None is None)
print(empty(xs))
xs = [1, 2]
print(xs is None)
print(None is xs)
ys = xs
print(ys is xs)
zs = [1, 2]
print(zs is xs)
print(xs + ys is xs)
print(ident(xs) is xs)
print(ident(zs) is xs)
bs = [True]
print(bs is None)
print(xs is bs)
print([] is None)
print(empty(xs))
print(empty([]))
ys = None
print(ys is None)
print(xs is ys)
print(not (xs is None) and xs[0] == 1)
print(ys is None or ys[0] == 1)
