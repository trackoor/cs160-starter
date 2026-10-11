# error: 6:16
# a comma in an argument list must be followed by another argument
def add(a: int, b: int) -> int:
    return a + b

print(add(1, 2,))
