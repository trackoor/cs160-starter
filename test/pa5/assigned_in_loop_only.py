# ir-lacks: alloca
# ir-count: = phi 3
def last_multiple(n: int, k: int) -> int:
    i: int = 1
    found: int = 0
    while i <= n:
        if i % k == 0:
            found = i
        i = i + 1
    return found

print(last_multiple(0, 3))
print(last_multiple(10, 3))
print(last_multiple(10, 4))
print(last_multiple(2, 5))
