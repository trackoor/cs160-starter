# error: 3:1
# int names a type, so it cannot also be declared as a variable
int: int = 0
x: int = 5
print(x + int)
