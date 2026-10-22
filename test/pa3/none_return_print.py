# Returning a valid built-in call is allowed in a function without -> T.
# Expected lines: 7, True, 8, 0; statements after the return must not execute.
# An unreachable loop back edge must not make --verify reject the function.
def report(n: int):
    return print(n)
    print(99)

def report_bool(flag: bool):
    return print(flag)

def first(n: int) -> int:
    while n > 0:
        return n * 2
        n = n - 1
    return 0

report(7)
report_bool(True)
print(first(4))
print(first(0))
