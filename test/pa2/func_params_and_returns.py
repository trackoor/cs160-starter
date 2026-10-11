# Functions with no, one and several parameters, with and without a return
# type, with list-typed parameters and results, and with unusual spacing.
def nothing():
    pass

def identity(x: int) -> int:
    return x

def several(a: int, b: bool, c: str, d: [int], e: [[bool]]) -> [str]:
    return [c]

def no_return_type(s: str):
    print(s)

def nested_list() -> [[int]]:
    return [[1]]

def spaced( a : int , b : int ) -> bool :
    return a < b

nothing()
print(identity(1))
print(several(1, True, "c", [2], [[False]])[0])
no_return_type("s")
print(len(nested_list()))
print(spaced(1, 2))
