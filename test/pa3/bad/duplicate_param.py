# error: 3:26
# the parameter w is declared twice
def area(w: int, h: int, w: int) -> int:
    return w * h

print(area(2, 3, 4))
