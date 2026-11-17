# ir-count: call i32 @fn\.tick\( 2
count: int = 0

def tick() -> int:
    global count
    count = count + 1
    return count

def two() -> int:
    return tick() + tick()

print(two())
