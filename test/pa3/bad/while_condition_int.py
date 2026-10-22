# error: 5:7
# a while condition must be a bool, but n is an int
n: int = 5
total: int = 0
while n:
    total = total + n
    n = n - 1
print(total)
