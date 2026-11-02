# expect-exit: 4
x: int = 0

def find(n: int) -> [int]:
    print(n)
    if n > 0:
        return [n, n + 1]

for x in find(3):
    print(x)
for x in find(0):
    print(x)
print(100)
