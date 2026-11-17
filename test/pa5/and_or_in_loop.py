# ir-lacks: alloca
def count_hits(xs: [int], lo: int, hi: int) -> int:
    hits: int = 0
    x: int = 0
    for x in xs:
        if x >= lo and x <= hi or x == 0:
            hits = hits + (10 if x % 2 == 0 else 1)
    return hits

def first_gap(xs: [int]) -> int:
    i: int = 1
    while i < len(xs) and xs[i] == xs[i - 1] + 1:
        i = i + 1
    return i

def any_negative(xs: [int]) -> bool:
    i: int = 0
    seen: bool = False
    while i < len(xs):
        seen = seen or xs[i] < 0
        i = i + 1
    return seen

print(count_hits([1, 2, 3, 0, 7, 8, 12], 2, 8))
print(count_hits([], 0, 0))
print(first_gap([3, 4, 5, 9, 10]))
print(first_gap([1]))
print(first_gap([6, 7, 8]))
print(any_negative([1, 2, 3]))
print(any_negative([1, -2, 3]))
print(any_negative([]))
