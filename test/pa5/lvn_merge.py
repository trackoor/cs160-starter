# ir-lacks: alloca
# ir-count: mul i32 (%a\.arg, %b\.arg|%b\.arg, %a\.arg) 1
# ir-count: add i32 (%a\.arg, %b\.arg|%b\.arg, %a\.arg) 1
def f(a: int, b: int) -> int:
    c: int = 0
    d: int = 0
    e: int = 0
    c = a
    d = a * b + c * b
    e = (a + b) * (c + b) - (a + b)
    return d * 3 + e

def g(p: int, q: int, up: bool) -> int:
    r: int = 0
    if up:
        r = p * q + 1
    else:
        r = p * q - 1
    return r + p * q

print(f(3, 4))
print(f(-5, 7))
print(g(3, 4, True))
print(g(3, 4, False))
