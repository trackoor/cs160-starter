# ir-lacks: alloca
# ir-lacks: sdiv
# ir-lacks: srem
def table() -> int:
    a: int = 0
    b: int = 2
    c: int = 3
    a = -7
    print(a // b)
    print(a % b)
    print(-a // -b)
    print(-a % -c)
    print(a // -c)
    print(a % -c)
    print(a * 3 // 7)
    print(-8 % 4)
    print(-a // c)
    return a // c

print(table())
