# error: 3:7
# a parameter cannot be named after a type either; the error is at the parameter
def f(bool: int) -> int:
    return bool

print(f(1))
