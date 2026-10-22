# Functions with zero to four parameters of mixed types; swapping two
# arguments changes the result.
def zero() -> int:
    return 42

def one(flag: bool) -> int:
    if flag:
        return 1
    return 0

def sub(a: int, b: int) -> int:
    return a - b

def choose(first: bool, a: int, b: int) -> int:
    if first:
        return a
    return b

def mix(a: int, up: bool, b: int, neg: bool) -> int:
    r: int = 0
    if up:
        r = a * 10 + b
    else:
        r = b * 10 + a
    if neg:
        r = -r
    return r

def implies(p: bool, q: bool) -> bool:
    return not p or q

print(zero())
print(one(True))
print(one(False))
print(sub(10, 3))
print(sub(3, 10))
print(choose(True, 5, 9))
print(choose(False, 5, 9))
print(mix(1, True, 2, False))
print(mix(1, False, 2, False))
print(mix(1, True, 2, True))
print(mix(3, False, 4, True))
print(implies(True, False))
print(implies(False, True))
print(sub(sub(20, 5), sub(8, 2)))
