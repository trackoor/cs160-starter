# Every call has its own parameters and locals: values computed before a
# recursive call are still there after it returns.
def weave(n: int) -> int:
    before: int = 0
    after: int = 0
    before = n * 10
    if n == 0:
        return 0
    after = weave(n - 1)
    print(before + n)
    return before + after

def alternate(n: int, up: bool) -> int:
    inner: int = 0
    if n == 0:
        return 0
    inner = alternate(n - 1, not up)
    if up:
        return inner + n
    return inner - n

def before(n: int) -> int:
    after: int = 7
    return n + after

print(weave(4))
print(alternate(5, True))
print(alternate(6, False))
print(before(1))
