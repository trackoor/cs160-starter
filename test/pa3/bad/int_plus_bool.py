# error: 4:12
# the right operand of + is a bool, but + needs two ints
def add_flag(n: int, flag: bool) -> int:
    return n + flag

print(add_flag(1, True))
