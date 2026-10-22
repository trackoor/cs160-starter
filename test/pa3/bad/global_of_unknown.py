# error: 8:5
# counter is a local variable of setup, not a global variable
def setup():
    counter: int = 0
    print(counter)

def bump():
    global counter
    print(2)

setup()
bump()
