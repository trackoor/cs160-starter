# error: 5:5
# show has no return type, so it returns None and cannot return n
def show(n: int):
    print(n)
    return n

show(1)
