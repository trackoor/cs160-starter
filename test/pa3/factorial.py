# fact(12) = 479001600 is the largest factorial that fits in 32 bits.
def fact(n: int) -> int:
    if n <= 1:
        return 1
    return n * fact(n - 1)

def fact_loop(n: int) -> int:
    result: int = 1
    while n > 1:
        result = result * n
        n = n - 1
    return result

i: int = 0
while i <= 12:
    print(fact(i))
    i = i + 1
print(fact(12) == fact_loop(12))
print(fact(12) // fact(10))
print(fact(5) - fact(4) * 5)
