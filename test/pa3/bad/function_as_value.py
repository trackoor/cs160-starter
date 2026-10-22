# error: 7:10
# square names a function, so it cannot be used as a value
def square(n: int) -> int:
    return n * n

result: int = 0
result = square
print(result)
