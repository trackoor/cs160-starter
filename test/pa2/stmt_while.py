# while loops: simple, with a not test, with a compound test, nested, and with
# a parenthesized test.
i: int = 0
j: int = 0
done: bool = False

while i < 3:
    i = i + 1

while not done:
    done = True

while i > 0 and not done or j == 5:
    j = 0
    while j < i:
        j = j + 1
        if j == 2:
            done = True
    i = i - 1

while (i < 10):
    i = i + 1
