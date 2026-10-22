# A function may assign to its parameters; the caller's variables keep
# their values.
x: int = 10

def inc_all(a: int, b: int, flag: bool) -> int:
    a = a + 1
    b = b * 2
    flag = not flag
    if flag:
        return a + b
    return a - b

def countdown_sum(n: int) -> int:
    total: int = 0
    while n > 0:
        total = total + n
        n = n - 1
    return total * 1000 + n

def swap_diff(a: int, b: int) -> int:
    t: int = 0
    t = a
    a = b
    b = t
    return a - b

y: int = 3
print(inc_all(x, y, False))
print(inc_all(x, y, True))
print(x)
print(y)
print(countdown_sum(x))
print(x)
print(swap_diff(x, y))
print(swap_diff(y, x))
