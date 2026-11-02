xss: [[int]] = None
inner: [int] = None
nones: [[bool]] = None
xss = [None, [1]]
print(len(xss))
print(xss[0] is None)
print(xss[1][0])
xss[0] = [5, 6]
print(xss[0][1])
xss[1] = None
print(xss[1] is None)
xss = [[1], None, [2, 3], []]
for inner in xss:
    if inner is None:
        print(-1)
    else:
        print(len(inner))
nones = [None, None]
print(len(nones))
print(nones[1] is None)
nones[0] = [True]
print(nones[0][0])
xss = [None]
print(xss[0] is None)
xss = xss + [[7]]
print(len(xss))
print(xss[1][0])
xss = [None] + [None]
print(len(xss))
