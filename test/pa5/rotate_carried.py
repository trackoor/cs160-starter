# ir-lacks: alloca
# ir-count: = phi 5
def rotate(n: int) -> int:
    a: int = 1
    b: int = 2
    c: int = 3
    t: int = 0
    while n > 0:
        t = a
        a = b
        b = c
        c = t
        n = n - 1
    return a * 1000 + b * 100 + c * 10 + t

print(rotate(0))
print(rotate(1))
print(rotate(2))
print(rotate(3))
print(rotate(7))
