# ir-lacks: alloca
def find(xs: [int], target: int) -> int:
    i: int = 0
    while i < len(xs):
        if xs[i] == target:
            return i
        i = i + 1
    return -1

def sign(x: int) -> int:
    if x < 0:
        return -1
    elif x == 0:
        return 0
    return 1

def clamp(x: int, lo: int, hi: int) -> int:
    if x < lo:
        x = lo
        return x * 10
    if x > hi:
        return hi * 10
    x = x + 1
    return x * 10

def pair_sum(xs: [int], t: int) -> int:
    i: int = 0
    j: int = 0
    while i < len(xs):
        j = i + 1
        while j < len(xs):
            if xs[i] + xs[j] == t:
                return i * 10 + j
            j = j + 1
        i = i + 1
    return -1

print(find([4, 8, 15, 16], 15))
print(find([4, 8, 15, 16], 5))
print(sign(-9))
print(sign(0))
print(sign(3))
print(clamp(-4, 0, 9))
print(clamp(12, 0, 9))
print(clamp(5, 0, 9))
print(pair_sum([1, 5, 9, 4], 13))
print(pair_sum([1, 2], 10))
