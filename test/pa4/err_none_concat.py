# expect-exit: 4
xs: [int] = None
ys: [int] = None

def left() -> [int]:
    print(1)
    return xs

def right() -> [int]:
    print(2)
    return ys

ys = [5, 6]
print(len(ys + ys))
ys = left() + right()
print(len(ys))
