i: int = 0
j: int = 0
count: int = 0
while i < 4:
    j = 0
    while j < i:
        count = count + j
        j = j + 1
    i = i + 1
print(count)
print(i * 10 + j)
