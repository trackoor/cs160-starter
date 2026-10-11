# error: 8:6
# the target of an assignment is a variable or an indexed expression, never a call
x: int = 1

def f(n: int) -> int:
    return n

f(x) = 2
