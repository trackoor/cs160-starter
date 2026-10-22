# A tail-recursive sum, and a version that is not tail-recursive.
def sum_to(n: int, acc: int) -> int:
    if n == 0:
        return acc
    return sum_to(n - 1, acc + n)

def sum_down(n: int) -> int:
    if n <= 0:
        return 0
    return n + sum_down(n - 1)

print(sum_to(0, 0))
print(sum_to(10, 0))
print(sum_to(100, 0))
print(sum_to(10, 1000))
print(sum_down(100))
print(sum_to(300, 0) == sum_down(300))
