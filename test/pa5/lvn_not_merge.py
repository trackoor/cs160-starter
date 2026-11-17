# ir-lacks: alloca
# ir-count: call i32 @fn\.noisy\(i32 %a\.arg\) 2
# ir-has: sub i32 %a\.arg, %b\.arg
# ir-has: sub i32 %b\.arg, %a\.arg
def noisy(x: int) -> int:
    print(x)
    return x

def f(a: int, b: int) -> int:
    p: int = 0
    q: int = 0
    lt: bool = False
    gt: bool = False
    p = a - b
    q = b - a
    lt = a < b
    gt = a > b
    print(lt)
    print(gt)
    return p * 100 + q + noisy(a) * noisy(a)

print(f(7, 3))
print(f(2, 9))
