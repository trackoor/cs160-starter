# error: 6:1
# the global variable twice has the same name as the function declared above it
def twice(n: int) -> int:
    return n * 2

twice: int = 0
print(twice(3))
