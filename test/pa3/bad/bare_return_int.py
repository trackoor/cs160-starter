# error: 5:9
# a bare return returns None, but half must return an int
def half(n: int) -> int:
    if n < 0:
        return
    return n // 2

print(half(4))
