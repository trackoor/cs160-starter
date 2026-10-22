# error: 8:1
# when x is 0, sign reaches its end without returning an int
def abs_value(x: int) -> int:
    if x < 0:
        return -x
    return x

def sign(x: int) -> int:
    if x > 0:
        return 1
    elif x < 0:
        return -1

print(sign(abs_value(-3)))
