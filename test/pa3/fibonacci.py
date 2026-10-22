# Naive recursive Fibonacci, with a global counting the calls.
calls: int = 0

def fib(n: int) -> int:
    global calls
    calls = calls + 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

def fib_loop(n: int) -> int:
    a: int = 0
    b: int = 1
    t: int = 0
    while n > 0:
        t = a + b
        a = b
        b = t
        n = n - 1
    return a

k: int = 0
while k <= 15:
    print(fib(k))
    k = k + 1
calls = 0
print(fib(10))
print(calls)
print(fib_loop(40))
print(fib(20) == fib_loop(20))
