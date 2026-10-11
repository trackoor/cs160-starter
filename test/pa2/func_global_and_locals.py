# A function body starts with global declarations and local variable
# declarations, in any order, followed by at least one statement.
total: int = 0
label: str = "total"
history: [int] = None

def add(n: int) -> int:
    global total
    step: int = 1
    global history
    old: int = 0
    names: [str] = None
    old = total
    total = total + n * step
    history = [old, total]
    return total

def reset():
    global total
    total = 0

def only_locals() -> str:
    first: str = "a"
    second: str = "b"
    return first + second

add(5)
reset()
print(add(2))
print(only_locals())
