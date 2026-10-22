# Recursion 500 calls deep (CPython's default limit is 1000).
deepest: int = 0

def descend(n: int, level: int) -> int:
    global deepest
    if level > deepest:
        deepest = level
    if n == 1:
        return 1
    return 1 + descend(n - 1, level + 1)

def triangle(n: int) -> int:
    if n == 1:
        return 1
    return n + triangle(n - 1)

print(descend(500, 1))
print(deepest)
print(triangle(500))
print(triangle(499) + 500 == triangle(500))
