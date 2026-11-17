# ir-lacks: alloca
def triangle(n: int) -> int:
    i: int = 0
    j: int = 0
    s: int = 0
    while i < n:
        j = 0
        while j <= i:
            s = s + j
            j = j + 1
        i = i + 1
    return s

print(triangle(0))
print(triangle(10))
