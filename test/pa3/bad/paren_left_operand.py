# error: 4:12
# * needs two ints, but b is a bool; the product starts at the parenthesis before n
def f(n: int, b: bool) -> int:
    return (n + 1) * b

print(f(1, True))
