xs: [int] = None
e: [int] = None
ys: [str] = None
zss: [[int]] = None
x: int = 5

def size(p: [int]) -> int:
    return len(p)

print(len([]))
print(size([]))
xs = []
print(len(xs))
for x in xs:
    print(x)
print(x)
e = []
xs = xs + e
print(len(xs))
print(len(e + e))
xs = e + [1] + e
print(len(xs))
print(xs[0])
print(xs is e)
for x in e + e:
    print(x)
print(x)
ys = []
ys = ys + ["a"]
print(ys[0])
print([] is [])
print(xs is None)
zss = [[], [1, 2], []]
print(len(zss))
print(len(zss[0]) + len(zss[1]) + len(zss[2]))
zss[1] = []
for xs in zss:
    print(len(xs))
print(len([[]]))
