# ir-lacks: alloca
def classify(x: int) -> int:
    return 1 if x < 0 else (2 if x == 0 else 3)

def all3(a: bool, b: bool, c: bool) -> bool:
    return a and b and c

def either(a: bool, b: bool, c: bool) -> bool:
    return a or (b and c)

print(classify(-5))
print(classify(0))
print(classify(9))
print(all3(True, True, True))
print(all3(True, False, True))
print(all3(False, True, True))
print(either(False, True, True))
print(either(False, True, False))
print(either(True, False, False))
