# A name means the declaration visible where the code is written.
# show reads the global x, never the x of the function that calls it,
# so a compiler that resolves names at the call site prints 22, not 12.
x: int = 1
y: bool = True

def show() -> int:
    return x

def show_flag() -> bool:
    return y

def run() -> int:
    x: int = 2
    return show() * 10 + x

def run_flag() -> bool:
    y: bool = False
    return show_flag() and not y

def param_named_x(x: int) -> int:
    return show() + x * 100

print(show())
print(run())
print(run_flag())
print(param_named_x(5))
x = 7
print(run())
print(param_named_x(3))
