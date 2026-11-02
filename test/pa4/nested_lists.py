grid: [[int]] = None
row: [int] = None
cube: [[[int]]] = None
table: [[str]] = None
words: [str] = None
w: str = ""
i: int = 0
j: int = 0
total: int = 0
grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(len(grid))
print(len(grid[1]))
print(grid[2][0])
grid[1][1] = 50
row = grid[1]
print(row[1])
row[2] = 60
print(grid[1][2])
while i < len(grid):
    j = 0
    while j < len(grid[i]):
        total = total + grid[i][j]
        j = j + 1
    i = i + 1
print(total)
for row in grid:
    print(row[0] + row[1] + row[2])
    row[0] = 0
print(grid[0][0] + grid[1][0] + grid[2][0])
grid[0] = [42]
print(len(grid[0]))
print(grid[0][0])
cube = [[[1, 2], [3]], [[4], [5, 6, 7]]]
print(cube[1][1][2])
print(len(cube[0]))
grid = cube[0]
grid[1] = [30, 31]
print(cube[0][1][1])
cube[1] = [None, [0]]
print(cube[1][0] is None)
print(len(cube[1][1]))
table = [["a", "b"], ["c"], []]
for words in table:
    print(len(words))
    for w in words:
        print(w)
print(table[0][1] + table[1][0])
