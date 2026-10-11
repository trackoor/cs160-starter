# error: 4:5
# function definitions cannot be nested
def outer() -> int:
    def inner() -> int:
        return 1
    return inner()
