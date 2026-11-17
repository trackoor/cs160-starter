# ir-lacks: alloca
# ir-count: = phi 6
def weave(n: int) -> int:
    i: int = 0
    j: int = 0
    base: int = 0
    total: int = 0
    while i < n:
        base = i * 10
        j = 0
        while j < i:
            total = total + base + j
            j = j + 1
        i = i + 1
    return total * 100 + base + j

print(weave(0))
print(weave(1))
print(weave(4))
print(weave(7))
