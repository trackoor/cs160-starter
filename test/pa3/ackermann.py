# Ackermann's function on tiny inputs; the globals m and n are shadowed
# by the parameters of ack.
def ack(m: int, n: int) -> int:
    if m == 0:
        return n + 1
    if n == 0:
        return ack(m - 1, 1)
    return ack(m - 1, ack(m, n - 1))

m: int = 0
n: int = 0
while m <= 3:
    n = 0
    while n <= 3:
        print(ack(m, n))
        n = n + 1
    m = m + 1
print(m * 10 + n)
