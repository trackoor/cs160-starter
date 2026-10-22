# first calls second and third, which the file defines later, and second
# reads limit, which is declared between two function definitions.
def first(n: int) -> int:
    return second(n) + third(n)

def second(n: int) -> int:
    return n * limit

limit: int = 3

def third(n: int) -> int:
    if n > 0:
        return first(n - 1)
    return 0

ready: bool = True

print(first(0))
print(first(1))
print(first(3))
print(ready and first(2) == 9)
