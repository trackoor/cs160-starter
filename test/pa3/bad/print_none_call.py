# error: 7:7
# greet has no return type, so it returns None, which print cannot print
def greet(n: int):
    print(n)

greet(1)
print(greet(2))
