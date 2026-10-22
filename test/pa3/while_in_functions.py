# Loops inside functions that change their parameters.
def collatz_steps(n: int) -> int:
    steps: int = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps = steps + 1
    return steps

def digit_sum(n: int) -> int:
    s: int = 0
    while n > 0:
        s = s + n % 10
        n = n // 10
    return s

def reverse_digits(n: int) -> int:
    r: int = 0
    while n > 0:
        r = r * 10 + n % 10
        n = n // 10
    return r

def isqrt(n: int) -> int:
    lo: int = 0
    hi: int = 0
    mid: int = 0
    hi = n + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid
    return lo

print(collatz_steps(1))
print(collatz_steps(6))
print(collatz_steps(27))
print(digit_sum(987654321))
print(reverse_digits(12345))
print(isqrt(0))
print(isqrt(99))
print(isqrt(100))
print(isqrt(10000))
