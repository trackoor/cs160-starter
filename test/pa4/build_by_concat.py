squares: [int] = None
evens: [int] = None
names: [str] = None
rows: [[int]] = None
i: int = 0
x: int = 0
squares = []
while i < 10:
    squares = squares + [i * i]
    i = i + 1
print(len(squares))
print(squares[9])
evens = []
for x in squares:
    if x % 2 == 0:
        evens = [x] + evens
print(len(evens))
for x in evens:
    print(x)
names = []
i = 0
while i < 3:
    names = names + ["n" + "abc"[i]]
    i = i + 1
print(names[0] + names[1] + names[2])
rows = []
i = 0
while i < 3:
    rows = rows + [squares]
    i = i + 1
rows[0][0] = 99
print(rows[2][0])
print(squares[0])
print(rows[0] is rows[1])
