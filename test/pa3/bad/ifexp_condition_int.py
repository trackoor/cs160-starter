# error: 4:18
# the condition of a conditional expression must be a bool, but n is an int
def pick(n: int) -> int:
    return 10 if n else 20

print(pick(1))
