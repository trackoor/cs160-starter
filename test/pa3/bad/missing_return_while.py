# error: 3:1
# a while loop does not count as returning on every path, even while True
def first_square_above(limit: int) -> int:
    i: int = 0
    while True:
        if i * i > limit:
            return i
        i = i + 1

print(first_square_above(10))
