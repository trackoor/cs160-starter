# ir-lacks: alloca
# ir-has: store i32 .*, ptr @gv\.count
count: int = 0

def tick() -> int:
    global count
    count = count + 1
    return count

def two() -> int:
    return tick() + tick()

print(two())
print(count)
