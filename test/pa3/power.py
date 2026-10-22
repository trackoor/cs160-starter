# Two recursive powers; fast_power keeps a local across its recursive call.
def power(base: int, exp: int) -> int:
    if exp == 0:
        return 1
    return base * power(base, exp - 1)

def fast_power(base: int, exp: int) -> int:
    half: int = 0
    if exp == 0:
        return 1
    half = fast_power(base, exp // 2)
    if exp % 2 == 0:
        return half * half
    return half * half * base

print(power(2, 10))
print(power(3, 0))
print(power(-2, 5))
print(power(-3, 4))
print(fast_power(2, 30))
print(fast_power(3, 19))
print(fast_power(7, 11))
print(fast_power(-5, 13))
print(power(10, 9) == fast_power(10, 9))
print(power(5, 3) - power(3, 5))
