# Arguments are evaluated left to right, before the call.
counter: int = 0

def show(n: int) -> int:
    print(n)
    return n

def tick() -> int:
    global counter
    counter = counter + 1
    return counter

def flag(b: bool) -> bool:
    print(b)
    return b

def sub3(a: int, b: int, c: int) -> int:
    return a - b - c

def pack(a: int, b: bool, c: int, d: bool) -> int:
    r: int = 0
    r = a * 100 + c
    if b:
        r = r + 10
    if d:
        r = r + 1
    return r

print(sub3(show(10), show(3), show(2)))
print(sub3(tick(), tick(), tick()))
print(tick() - tick())
print(pack(show(1), flag(True), show(2), flag(False)))
print(sub3(show(sub3(show(9), show(1), show(1))), tick(), show(0)))
print(counter)
