# ir-lacks: alloca
def pick(flag: bool, a: int, b: int) -> int:
    r: int = 0
    if flag:
        r = a - b
    else:
        r = b - a
    return r * 10

print(pick(True, 7, 2))
print(pick(False, 7, 2))
