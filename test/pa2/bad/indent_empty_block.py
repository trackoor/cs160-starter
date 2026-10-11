# error: 7:5
# the inner if's block is empty: line 7 closes blocks instead of opening one (DEDENT at its first token)
x: int = 0
while x < 3:
    while x < 2:
        if x == 1:
    x = x + 1
