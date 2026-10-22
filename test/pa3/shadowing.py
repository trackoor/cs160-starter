# Parameters and locals shadow globals, and even global functions.
n: int = 1000
flag: bool = False

def square(n: int) -> int:
    return n * n

def local_n() -> int:
    n: int = 5
    n = n + 1
    return n

def uses_both(k: int) -> int:
    flag: bool = True
    if flag:
        return k + n
    return k

def square_shadowed() -> int:
    square: int = 9
    return square + 1

def param_shadows_function(square: int) -> int:
    return square - 1

print(square(12))
print(local_n())
print(n)
print(uses_both(3))
print(flag)
print(square_shadowed())
print(param_shadows_function(50))
print(square(3))
