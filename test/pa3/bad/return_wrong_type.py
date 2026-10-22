# error: 4:5
# is_big must return a bool, but n * 2 is an int
def is_big(n: int) -> bool:
    return n * 2

print(is_big(3))
