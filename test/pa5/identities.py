# ir-lacks: alloca
# ir-lacks: mul i32 %\S+, 1$
# ir-lacks: add i32 %\S+, 0$
# ir-has: ret i32 %x\.arg$
def same(x: int) -> int:
    one: int = 1
    zero: int = 0
    y: int = 0
    y = x * one + zero
    return y * one + zero

def negate(x: int) -> int:
    zero: int = 0
    return zero - x

def accumulate(n: int) -> int:
    i: int = 0
    s: int = 0
    step: int = 1
    while i < n:
        s = s + i * step + 0
        i = i + step
    return s

print(same(42))
print(same(-3))
print(negate(8))
print(negate(-8))
print(accumulate(5))
