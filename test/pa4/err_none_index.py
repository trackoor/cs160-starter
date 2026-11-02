# expect-exit: 4
xs: [int] = None

def say(n: int) -> int:
    print(n)
    return n

xs = [10, 20]
print(xs[say(1)])
xs = None
print(xs[say(0)])
print(99)
