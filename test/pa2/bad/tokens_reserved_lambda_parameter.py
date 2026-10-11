# error: 3:15
# lambda is a reserved word even though ChocoPy never uses it, so it cannot name a parameter
def f(x: int, lambda: int) -> int:
    return x
