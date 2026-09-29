n: int = 2
d: int = 0
prime: bool = True
count: int = 0
while n < 200:
    d = 2
    prime = True
    while d * d <= n and prime:
        if n % d == 0:
            prime = False
        d = d + 1
    if prime:
        count = count + 1
    n = n + 1
print(count)
