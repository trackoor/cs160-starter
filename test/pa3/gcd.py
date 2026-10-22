# Euclid's algorithm, by remainder and by subtraction; argument order matters.
def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)

def gcd_sub(a: int, b: int) -> int:
    if a == b:
        return a
    if a > b:
        return gcd_sub(a - b, b)
    return gcd_sub(a, b - a)

def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b

print(gcd(48, 18))
print(gcd(18, 48))
print(gcd(17, 5))
print(gcd(0, 9))
print(gcd(9, 0))
print(gcd(1071, 462))
print(gcd_sub(1071, 462))
print(gcd_sub(35, 14))
print(lcm(4, 6))
print(lcm(21, 6))
print(gcd(2147483646, 1073741823))
