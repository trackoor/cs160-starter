# error: 7:9
# the int parameter n is assigned the bool n > 10
def clamp(n: int) -> int:
    if n < 0:
        n = 0
    else:
        n = n > 10
    return n

print(clamp(5))
