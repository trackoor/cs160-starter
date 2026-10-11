# if, if-else, if-elif, and a long if-elif-else chain. Each elif becomes an If,
# starting at the elif keyword, in the orelse of the If before it; an if
# written inside an else block is a separate statement in that block.
x: int = 3

if x == 1:
    print(1)

if x == 1:
    print(1)
else:
    print(2)

if x == 1:
    print(1)
elif x == 2:
    print(2)

if x == 1:
    print(1)
elif x == 2:
    print(2)
elif x == 3:
    print(3)
elif x == 4:
    print(4)
else:
    print(5)

if x == 1:
    print(1)
else:
    if x == 2:
        print(2)
    else:
        print(3)
    print(4)

if x > 0:
    if x > 1:
        print(2)
    elif x > 2:
        pass
else:
    pass
