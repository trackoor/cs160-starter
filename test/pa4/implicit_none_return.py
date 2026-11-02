xs: [int] = None

def maybe(n: int) -> [int]:
    if n > 0:
        return [n, n]

def nothing() -> [str]:
    pass

def early(p: [int]) -> [int]:
    x: int = 0
    for x in p:
        if x < 0:
            return
    return p

def first_or_none(p: [int]) -> [int]:
    if len(p) == 0:
        return None
    return [p[0]]

print(maybe(3) is None)
print(maybe(0) is None)
print(len(maybe(2)))
print(nothing() is None)
print(early([1, -2, 3]) is None)
xs = [4, 5]
print(early(xs) is xs)
xs = maybe(-1)
print(xs is None)
print(first_or_none([]) is None)
print(first_or_none([7, 8])[0])
xs = maybe(1)
print(xs[1])
