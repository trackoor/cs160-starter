# expect-exit: 2
# ir-lacks: alloca
# ir-has: call void @cp_error_div
# ir-count: sdiv i32 100, 0 1
# ir-count: srem i32 100, 0 1
def risky(flag: bool) -> int:
    d: int = 0
    r: int = 1
    if flag:
        r = 100 // d
    return r

print(risky(False))
print(risky(True))
