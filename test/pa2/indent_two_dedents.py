# Before print(0) the lexer must close two blocks at once (the handout's
# example); before else it closes the inner if and the while in one step.
x: int = 3
if True:
    if False:
        print(1 + 2 * 3)
print(0)
if x > 0:
    while x > 0:
        if x == 2:
            print(x)
        x = x - 1
else:
    print(x)
