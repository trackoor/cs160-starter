# ir-lacks: alloca
# ir-count: = phi 3
def total(n: int, choose: bool) -> int:
    i: int = 0
    acc: int = 0
    extra: int = 10
    if choose:
        extra = 1
    while i < n:
        acc = acc + extra
        i = i + 1
    return acc

print(total(3, True))
print(total(3, False))
