# Calls nested inside the arguments of other calls.
def add(a: int, b: int) -> int:
    return a + b

def mul(a: int, b: int) -> int:
    return a * b

def neg(a: int) -> int:
    return -a

def max2(a: int, b: int) -> int:
    return a if a > b else b

def is_pos(a: int) -> bool:
    return a > 0

print(add(mul(2, 3), mul(4, 5)))
print(mul(add(1, 2), add(3, neg(4))))
print(max2(max2(3, 9), max2(neg(1), 7)))
print(add(add(add(1, 2), add(3, 4)), add(add(5, 6), add(7, 8))))
print(is_pos(add(neg(5), mul(2, 3))))
print(neg(neg(neg(max2(add(1, 1), mul(1, 1))))))
print(add(mul(add(1, 2), 3), 4) - mul(2, add(3, 4)))
