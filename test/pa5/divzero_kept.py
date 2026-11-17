# expect-exit: 2
# ir-has: call void @cp_error_div
def f(d: int) -> int:
    k: int = 0
    k = 100 // d
    return k

print(f(5))
print(f(0))
