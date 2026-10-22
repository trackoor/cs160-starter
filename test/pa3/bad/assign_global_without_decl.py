# error: 6:5
# bump assigns to the global count without declaring it global
count: int = 0

def bump(n: int) -> int:
    count = count + n
    return count

print(bump(5))
