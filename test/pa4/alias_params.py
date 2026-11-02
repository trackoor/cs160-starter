data: [int] = None
log: [int] = None
count: int = 0

def fill(xs: [int], v: int):
    i: int = 0
    while i < len(xs):
        xs[i] = v + i
        i = i + 1

def rebind(xs: [int]):
    xs = [100, 200, 300, 400]
    xs[0] = 0

def swap(xs: [int], i: int, j: int):
    tmp: int = 0
    tmp = xs[i]
    xs[i] = xs[j]
    xs[j] = tmp

def record(v: int):
    global log
    global count
    log = log + [v]
    count = count + 1

def bump_first():
    data[0] = data[0] + 1

def same(a: [int], b: [int]) -> bool:
    a[0] = 111
    return b[0] == 111

data = [0, 0, 0, 0]
log = []
fill(data, 10)
print(data[0])
print(data[3])
rebind(data)
print(data[0])
swap(data, 0, 3)
print(data[0])
print(data[3])
bump_first()
print(data[0])
record(data[1])
record(data[2])
print(count)
print(len(log))
print(log[1])
print(same(data, data))
print(same(data, [1, 2]))
print(data[0])
