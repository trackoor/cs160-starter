# Calls with no, one and several arguments; each argument is a full expression,
# including conditional expressions, boolean operators and nested calls.
x: int = 0

def zero() -> int:
    return 0

def one(a: int) -> int:
    return a

def three(a: int, b: bool, c: str) -> int:
    return a

x = zero()
x = one(1)
x = three(1, True, "s")
x = three(one(zero()), not True, "a" + "b")
x = one(x if x > 0 else -x)
x = three(x + 1, x == 1 or x == 2, "")
print(len("abc"))
print(one(zero() + one(1) * three(2, False, "c")))
zero()
