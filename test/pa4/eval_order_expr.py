xs: [int] = None

def say(n: int) -> int:
    print(n)
    return n

def lst(n: int) -> [int]:
    print(n)
    return [n]

def echo(w: str) -> str:
    print(w)
    return w

def three(a: int, b: int, c: int) -> int:
    return a * 100 + b * 10 + c

print(three(say(1), say(2), say(3)))
xs = [say(4), say(5), say(6)]
print(len(xs))
xs = lst(7) + lst(8)
print(xs[1])
print(echo("a") + echo("b"))
print(lst(9)[say(0)])
print(say(1) - say(2) * say(3))
print(len(lst(4) + lst(5) + lst(6)))
print(echo("x") == echo("y"))
print(lst(1) is lst(2))
