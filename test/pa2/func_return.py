# return with and without a value, at the end of a body and inside nested
# blocks; the value may be any expression.
def sign(n: int) -> int:
    if n > 0:
        return 1
    elif n < 0:
        return -1
    return 0

def show(n: int):
    if n == 0:
        return
    print(n)
    return

def first(xs: [int]) -> int:
    x: int = 0
    for x in xs:
        return x
    return -1

def pick(b: bool, xs: [int]) -> [int]:
    while b:
        return [1, 2]
    return xs if not b else []

def negate(b: bool) -> bool:
    return not b

show(sign(-5))
print(first([3, 4]))
print(len(pick(negate(True), [])))
