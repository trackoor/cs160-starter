# error: 6:5
# the local variable total is declared twice in one function
def f(n: int) -> int:
    total: int = 0
    count: int = 0
    total: int = 1
    total = total + n
    return total + count

print(f(2))
