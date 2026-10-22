# local_value has a local named value; setter changes the global value.
# The two must stay separate even though one function calls the other.
value: int = 1

def setter(n: int):
    global value
    value = n

def getter() -> int:
    return value

def local_value() -> int:
    value: int = 50
    setter(7)
    value = value + 1
    return value * 100 + getter()

def same_names_elsewhere(value: int) -> int:
    setter(value + 1)
    return value * 100 + getter()

print(getter())
print(local_value())
print(value)
print(same_names_elsewhere(3))
print(value)
