# error: 4:5
# None is not compatible with str: strings are never None.
def f() -> int:
    s: str = None
    return len(s)

print(f())
