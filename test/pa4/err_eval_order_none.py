# expect-exit: 4
def say(n: int) -> int:
    print(n)
    return n

xs: [int] = None
xs[say(1)] = say(2)
print(3)
