# Declarations of every type, each initialized with a literal: int, bool, str,
# and list types (initialized with None) nested up to three levels. Spaces
# inside a type are allowed.
i: int = 42
t: bool = True
f: bool = False
s: str = "chocopy"
e: str = ""
xs: [int] = None
bs: [bool] = None
ss: [str] = None
xss: [[int]] = None
bss: [ [ bool ] ] = None
sss: [[[str]]] = None

def typed(a: [[int]], b: [str]) -> [[[str]]]:
    return sss

print(i)
