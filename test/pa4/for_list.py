xs: [int] = None
x: int = 0
y: int = 0
total: int = 0
count: int = 0
xs = [3, 1, 4, 1, 5, 9, 2, 6]
for x in xs:
    total = total + x
print(total)
print(x)
for x in [10, 20, 30]:
    print(x)
for x in xs:
    if x > 4:
        print(x)
for x in xs:
    xs = [0]
    total = total + x
print(total)
print(len(xs))
for x in [1, 2, 3]:
    for y in [1, 2, 3]:
        if x < y:
            count = count + 1
print(count)
for x in [7]:
    x = x * 2
    print(x)
print(x)
