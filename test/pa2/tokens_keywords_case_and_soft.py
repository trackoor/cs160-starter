# Keywords are case-sensitive (true, NONE and If are identifiers), and Python's
# soft keywords match, case, type and _ are ordinary identifiers in ChocoPy.
true: bool = False
false: bool = True
none: [int] = None
NONE: int = 0
If: int = 1
Not: bool = False
AND: int = 2
Def: str = "def"
match: int = 3
case: str = "case"
type: int = 4
_: int = 5
__init__: int = 6
x_1_y2: int = 7
xor: bool = True
motif: int = 8
True_: bool = True

def ELSE(If: int, match: int) -> bool:
    return If == match

if ELSE(If, match) or not Not:
    print(case)
    none = [If, AND, type, _, NONE]
print(Def + case)
xor = true == false and True_
match = __init__ + x_1_y2 * motif
