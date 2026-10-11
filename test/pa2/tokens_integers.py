# Integer literals from 0 up to the largest one, 2147483647. There are no
# negative literals: -2147483647 is unary minus applied to 2147483647.
zero: int = 0
biggest: int = 2147483647
one: int = 1
ten: int = 10
x: int = 1000000000

x = -2147483647
x = biggest - 2147483647
x = 0 + 0 * 0
x = 2147483647 // 10 % 7
x = -0
x = - 1
x = 100 - 99
print(biggest)
print(len([0, 1, 10, 2147483647]))
