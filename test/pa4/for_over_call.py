calls: int = 0

def make(n: int) -> [int]:
    global calls
    xs: [int] = None
    i: int = 0
    calls = calls + 1
    print(100 + n)
    xs = []
    while i < n:
        xs = xs + [i * i]
        i = i + 1
    return xs

def words() -> [str]:
    return ["x", "yy", "zzz"]

x: int = 0
w: str = ""
for x in make(4):
    print(x)
print(calls)
for w in words():
    print(len(w))
print(make(3)[2])
print(len(make(0)))
for x in make(0):
    print(x)
print(calls)
