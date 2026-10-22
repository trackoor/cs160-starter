# error: 6:1
# f is a function, not a variable, so it cannot be assigned
def f() -> int:
    return 1

f = 2
print(f())
