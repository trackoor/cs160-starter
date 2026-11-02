def rng(n: int) -> [int]:
    xs: [int] = None
    i: int = 0
    xs = []
    while i < n:
        xs = xs + [i]
        i = i + 1
    return xs

def total(xs: [int]) -> int:
    s: int = 0
    x: int = 0
    for x in xs:
        s = s + x
    return s

def doubled(xs: [int]) -> [int]:
    out: [int] = None
    x: int = 0
    out = []
    for x in xs:
        out = out + [2 * x]
    return out

def tail(xs: [int]) -> [int]:
    out: [int] = None
    i: int = 1
    out = []
    while i < len(xs):
        out = out + [xs[i]]
        i = i + 1
    return out

def rev(xs: [int]) -> [int]:
    if len(xs) == 0:
        return []
    return rev(tail(xs)) + [xs[0]]

def flatten(xss: [[int]]) -> [int]:
    out: [int] = None
    xs: [int] = None
    out = []
    for xs in xss:
        if not (xs is None):
            out = out + xs
    return out

def show(xs: [int]):
    x: int = 0
    for x in xs:
        print(x)

def join(ws: [str], sep: str) -> str:
    out: str = ""
    i: int = 0
    while i < len(ws):
        if i > 0:
            out = out + sep
        out = out + ws[i]
        i = i + 1
    return out

print(total(rng(5)))
print(total(doubled(rng(5))))
print(len(doubled([])))
print(total(doubled(doubled([1, 2, 3]))))
show(rev([1, 2, 3, 4]))
show(flatten([[1, 2], None, [], [3]]))
print(len(flatten([])))
print(len(rev(rng(0))))
print(join(["a", "b", "c"], ", "))
print(join([], "-"))
print(rev(rng(3))[0])
