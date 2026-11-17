# ir-lacks: alloca
def fib(n: int) -> int:
    a: int = 0
    b: int = 1
    t: int = 0
    while n > 0:
        t = a + b
        a = b
        b = t
        n = n - 1
    return a

print(fib(0))
print(fib(1))
print(fib(30))
