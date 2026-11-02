xs: [int] = None
ys: [int] = None

def say(n: int) -> int:
    print(n)
    return n

def pick(which: int) -> [int]:
    print(100 + which)
    if which == 0:
        return xs
    return ys

def grow() -> int:
    global xs
    xs = [9, 9, 9, 9]
    return 1

xs = [0, 0, 0]
ys = [0, 0, 0]
xs[say(1)] = say(2)
print(xs[1])
pick(say(0))[say(2)] = say(7)
print(xs[2])
pick(1)[say(0)] = pick(0)[say(1)] + say(10)
print(ys[0])
xs[xs[0]] = say(xs[0] + 5)
print(xs[0])
xs = [0, 0]
xs[3] = grow()
print(xs[3])
print(len(xs))
