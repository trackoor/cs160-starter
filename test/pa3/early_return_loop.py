# Returns from inside while loops, including nested ones.
def first_divisor(n: int) -> int:
    d: int = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d = d + 1
    return n

def find_square_above(limit: int) -> int:
    i: int = 0
    while True:
        if i * i > limit:
            return i
        i = i + 1
    return -1

def count_until_negative(start: int, step: int) -> int:
    steps: int = 0
    while start >= 0:
        start = start - step
        steps = steps + 1
        if steps > 1000:
            return -1
    return steps

def pair_with_product(p: int, s: int) -> int:
    a: int = 1
    b: int = 1
    while a <= p:
        b = a
        while b <= p:
            if a * b == p and a + b == s:
                return a * 100 + b
            b = b + 1
        a = a + 1
    return 0

print(first_divisor(91))
print(first_divisor(97))
print(first_divisor(1001))
print(find_square_above(50))
print(find_square_above(0))
print(count_until_negative(10, 3))
print(count_until_negative(5, 0))
print(pair_with_product(36, 13))
print(pair_with_product(36, 14))
