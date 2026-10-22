# Functions without a return type return None; they are called as
# statements, and a bare return leaves them early. noisy returns an int
# that the caller throws away.
total: int = 0

def report(n: int, big: bool):
    print(n)
    if big:
        print(n > 100)

def add_to_total(n: int):
    global total
    if n < 0:
        return
    total = total + n

def countdown(n: int):
    while n > 0:
        print(n)
        n = n - 1
    return

def nothing():
    pass

def noisy(n: int) -> int:
    print(n)
    return n * 2

report(7, False)
report(150, True)
add_to_total(5)
add_to_total(-3)
add_to_total(10)
print(total)
countdown(3)
nothing()
noisy(4)
print(total + noisy(5))
