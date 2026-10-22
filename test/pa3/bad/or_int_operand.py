# error: 4:12
# or needs bool operands, but n is an int
def either(b: bool, n: int) -> bool:
    return b or n

print(either(True, 1))
