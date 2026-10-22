# error: 5:1
# print is predefined, so a function named print declares it a second time
x: int = 1

def print(n: int):
    pass

print(x)
