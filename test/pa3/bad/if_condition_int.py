# error: 4:8
# an if condition must be a bool, but n % 2 is an int
def parity(n: int) -> int:
    if n % 2:
        return 1
    return 0

print(parity(3))
