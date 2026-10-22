# error: 8:16
# the second argument of scale must be a bool, but 7 - 2 is an int
def scale(n: int, negate: bool) -> int:
    if negate:
        return -n
    return n

print(scale(3, 7 - 2))
