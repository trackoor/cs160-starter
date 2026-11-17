# ir-lacks: alloca
def total(xs: [int]) -> int:
    s: int = 0
    x: int = 0
    for x in xs:
        s = s + x
    return s

print(total([1, 2, 3, 4]))
print(total([]))
