# error: 5:1
# the function total has the same name as the global variable total
total: int = 0

def total() -> int:
    return 1

print(total)
