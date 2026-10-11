# error: 5:1
# elif must continue an if statement, but here it follows an assignment
x: int = 0
x = 1
elif x == 1:
    print(x)
