xs: [int] = None
ys: [int] = None
i: int = 0
n: int = 0
c: bool = True
xs = [0, 0, 0, 0, 0, 0, 0, 0]
n = len(xs)
while i < n:
    xs[(i * 3) % n] = i
    i = i + 1
i = 0
while i < n:
    print(xs[i])
    i = i + 1
print(xs[xs[3]])
xs[xs[1] // 2] = xs[n - 1] * 10
print(xs[1])
print(xs[len(xs) - 1 - xs[0]])
print([10, 20, 30][xs[3] + 1])
print("abcdefgh"[xs[2]])
ys = [1, 2, 3]
(xs if c else ys)[0] = 11
c = False
(xs if c else ys)[0] = 44
print(xs[0])
print(ys[0])
print((ys if c else xs)[1])
