# error: 7:1
# A user function keeps its return type despite a wrong argument count.
def number(n: int) -> int:
    return n

flag: bool = False
flag = number()
