# // and % round toward negative infinity, also on values passed as arguments.
def floor_div(a: int, b: int) -> int:
    return a // b

def modulo(a: int, b: int) -> int:
    return a % b

def consistent(a: int, b: int) -> bool:
    return floor_div(a, b) * b + modulo(a, b) == a

print(floor_div(7, 2))
print(floor_div(-7, 2))
print(floor_div(7, -2))
print(floor_div(-7, -2))
print(modulo(7, 3))
print(modulo(-7, 3))
print(modulo(7, -3))
print(modulo(-7, -3))
print(consistent(-17, 5) and consistent(17, -5) and consistent(-17, -5))
