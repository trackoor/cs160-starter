# ir-lacks: alloca
def check(x: int) -> bool:
    return x != 0 and 100 // x > 5 or x == -1

print(check(0))
print(check(10))
print(check(50))
print(check(-1))
print(3 if check(4) else 4)
