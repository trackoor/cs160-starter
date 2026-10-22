# error: 6:5
# count is already a parameter of f, so global count declares it twice
count: int = 0

def f(count: int):
    global count
    print(count)

f(1)
