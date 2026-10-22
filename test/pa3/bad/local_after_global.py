# error: 7:5
# after global x, a local declaration of x declares x twice in f
x: int = 0

def f():
    global x
    x: int = 1
    print(x)

f()
