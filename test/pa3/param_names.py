# Parameters named like the IR's own names (t1, entry). A compiler that names an
# incoming argument %t1 or %entry produces IR that clang rejects; the course
# convention names it %t1.arg, which no ChocoPy name can collide with.
def f(t1: int, entry: int) -> int:
    t2: int = 0
    t2 = t1 * 10 + entry
    return t2

def g(t3: bool, addr: int) -> int:
    if t3:
        return addr
    return -addr

print(f(4, 2))
print(g(True, 7))
print(g(False, 7))
