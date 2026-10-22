# A conditional expression evaluates its condition, then exactly one branch.
def loud(n: int) -> int:
    print(n)
    return n

def check(n: int) -> bool:
    print(n)
    return n > 0

def pick(c: bool, a: int, b: int) -> int:
    return a if c else b

def sign(n: int) -> int:
    return 1 if n > 0 else -1 if n < 0 else 0

print(loud(1) if check(5) else loud(2))
print(loud(3) if check(-5) else loud(4))
print(pick(True, 10, 20))
print(pick(False, 10, 20))
print(sign(7) * 100 + sign(-7) * 10 + sign(0))
print(check(1) if check(0) else check(2))
