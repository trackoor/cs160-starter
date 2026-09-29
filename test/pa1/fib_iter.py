a: int = 0
b: int = 1
i: int = 0
t: int = 0
while i < 40:
    t = a + b
    a = b
    b = t
    i = i + 1
print(a)
