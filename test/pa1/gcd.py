a: int = 1071
b: int = 462
t: int = 0
while b != 0:
    t = b
    b = a % b
    a = t
print(a)
