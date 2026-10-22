# error: 5:16
# < compares two ints, but True is a bool
def check(n: int) -> bool:
    if n > 0:
        return 1 < True
    return False

print(check(1))
