# and, or and conditional expressions evaluate only the operands they
# need; each call prints its argument, so skipped calls print nothing.
calls: int = 0

def yes(n: int) -> bool:
    global calls
    calls = calls + 1
    print(n)
    return True

def no(n: int) -> bool:
    global calls
    calls = calls + 1
    print(n)
    return False

print(no(1) and yes(2))
print(yes(3) or no(4))
print(yes(5) and no(6) and yes(7))
print(no(8) or no(9) or yes(10))
print(no(11) or yes(12) and no(13))
print(not yes(14) and yes(15))
if yes(16) or yes(17):
    print(calls)
print(yes(18) if no(19) else no(20))
print(calls)
