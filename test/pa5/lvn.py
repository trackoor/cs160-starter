# ir-count: add i32 (?:%[-\w$.]+, 1|1, %[-\w$.]+)[ \t]*$ 1
# ir-lacks: mul i32 3, 4
def f(x: int) -> int:
    y: int = 0
    z: int = 0
    y = (x + 1) * 2
    z = (x + 1) * 2 + 3 * 4
    return y + z

print(f(5))
print(f(-3))
