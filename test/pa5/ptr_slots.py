# ir-lacks: alloca
# ir-has: = phi ptr
def squares(n: int) -> [int]:
    xs: [int] = None
    i: int = 0
    xs = []
    while i < n:
        xs = xs + [i * i]
        i = i + 1
    return xs

def pick(flag: bool) -> str:
    s: str = "left"
    t: str = "right"
    u: str = ""
    if flag:
        u = s
    else:
        u = t
    return u + "!"

def maybe(n: int) -> [int]:
    r: [int] = None
    if n > 0:
        r = [n, n + 1]
    return r

def total(xs: [int]) -> int:
    s: int = 0
    x: int = 0
    if xs is None:
        return -1
    for x in xs:
        s = s + x
    return s

print(total(squares(5)))
print(len(squares(0)))
print(pick(True))
print(pick(False))
print(total(maybe(3)))
print(total(maybe(0)))
print(maybe(0) is None)
