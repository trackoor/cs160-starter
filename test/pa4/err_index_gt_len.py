# expect-exit: 3
xs: [bool] = None

def say(n: int) -> int:
    print(n)
    return n

xs = [True, False]
print(xs[1])
xs[say(1)] = True
print(xs[1])
xs[say(5)] = say(0) == 0
print(xs[0])
