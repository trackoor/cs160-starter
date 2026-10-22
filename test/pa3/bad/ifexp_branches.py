# error: 4:12
# the branches of the conditional expression are an int and a bool
def f(n: int) -> int:
    return n if n > 0 else n > -5

print(f(1))
