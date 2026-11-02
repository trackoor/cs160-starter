# expect-exit: 3
data: [int] = None
k: int = 0
total: int = 0

def get(xs: [int], i: int) -> int:
    print(i)
    return xs[i]

data = [1, 2, 3]
for k in [0, 2, 1, 3, 0]:
    total = total + get(data, k)
    print(total)
print(total)
