# error: 7:5
# global must name a global variable, but helper is a function
def helper() -> int:
    return 1

def f():
    global helper
    print(helper())

f()
