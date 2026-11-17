# ir-lacks: alloca
# ir-has: store i32 %\S+, ptr @gv\.level
# ir-count: load i32, ptr @gv\.level 4
# ir-count: call i32 @fn\.bump\(i32 1\) 3
level: int = 0

def bump(d: int) -> int:
    global level
    level = level + d
    return d * 2

def probe() -> int:
    before: int = 0
    after: int = 0
    before = level
    bump(1)
    after = level
    return after * 10 + before

def twice() -> int:
    return bump(1) * 100 + bump(1)

print(probe())
print(twice())
print(probe())
print(level)
