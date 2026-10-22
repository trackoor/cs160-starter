# Boolean parameters and results; the globals a, b and c share their
# names with parameters.
def xor(a: bool, b: bool) -> bool:
    return a != b

def majority(a: bool, b: bool, c: bool) -> bool:
    return a and b or a and c or b and c

def to_int(b: bool) -> int:
    if b:
        return 1
    return 0

def encode(a: bool, b: bool, c: bool) -> int:
    return to_int(a) * 4 + to_int(b) * 2 + to_int(c)

def same(a: bool, b: bool) -> bool:
    return a == b

i: int = 0
a: bool = False
b: bool = False
c: bool = False
while i < 8:
    a = i // 4 == 1
    b = i // 2 % 2 == 1
    c = i % 2 == 1
    print(encode(a, b, c) * 10 + to_int(majority(a, b, c)))
    i = i + 1
print(xor(True, False))
print(xor(True, True))
print(same(xor(a, b), xor(b, a)))
print(encode(c, False, True))
