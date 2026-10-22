# error: 4:16
# unary minus needs an int operand, but True is a bool
def f(n: int) -> int:
    return n + -True

print(f(1))
