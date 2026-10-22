# error: 8:12
# g reads secret, a local variable of f that is not visible in g
def f() -> int:
    secret: int = 42
    return secret

def g() -> int:
    return secret

print(f() + g())
