# error: 7:1
# a function body needs a statement after its declarations; the file ends first
x: int = 0
def f() -> int:
    global x
    y: int = 1
