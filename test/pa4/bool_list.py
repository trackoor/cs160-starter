flags: [bool] = None
more: [bool] = None
sieve: [bool] = None
b: bool = False
count: int = 0
i: int = 0
j: int = 0
n: int = 30
flags = [True, False, True]
print(flags[0])
print(flags[1])
flags[1] = not flags[1]
print(flags[1])
more = flags + [False, False]
print(len(more))
for b in more:
    if b:
        count = count + 1
print(count)
print(more[4])
more[4] = more[0] and more[2]
print(more[4])
print(flags[2] == more[2])
sieve = []
while i <= n:
    sieve = sieve + [i >= 2]
    i = i + 1
i = 2
while i * i <= n:
    if sieve[i]:
        j = i * i
        while j <= n:
            sieve[j] = False
            j = j + i
    i = i + 1
i = 0
count = 0
for b in sieve:
    if b:
        print(i)
        count = count + 1
    i = i + 1
print(count)
