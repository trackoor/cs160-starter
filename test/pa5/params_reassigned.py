# ir-lacks: alloca
def gcd(a: int, b: int) -> int:
    t: int = 0
    while b != 0:
        t = a % b
        a = b
        b = t
    return a

def adjust(x: int, flag: bool) -> int:
    if flag:
        x = x + 100
    else:
        flag = x > 5
    if flag:
        x = x * 2
    return x

def countdown(n: int) -> int:
    s: int = 0
    while n > 0:
        s = s + n
        n = n - 2
    return s * 10 + n

print(gcd(48, 18))
print(gcd(7, 0))
print(gcd(17, 5))
print(adjust(3, True))
print(adjust(3, False))
print(adjust(9, False))
print(countdown(7))
print(countdown(8))
print(countdown(0))
