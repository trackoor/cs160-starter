a: int = 0
b: int = 0
a = -9
while a <= 9:
    b = -4
    while b <= 4:
        if b != 0:
            print(a // b)
            print(a % b)
        b = b + 1
    a = a + 1
