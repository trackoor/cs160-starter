# error: 6:1
# else must continue an if statement; ChocoPy has no while ... else
x: int = 0
while x < 3:
    x = x + 1
else:
    print(x)
