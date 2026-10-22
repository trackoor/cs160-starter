# Mutual recursion: each function calls the other, which is defined
# before or after it in the file.
def is_even(n: int) -> bool:
    if n == 0:
        return True
    return is_odd(n - 1)

def is_odd(n: int) -> bool:
    if n == 0:
        return False
    return is_even(n - 1)

def female(n: int) -> int:
    if n == 0:
        return 1
    return n - male(female(n - 1))

def male(n: int) -> int:
    if n == 0:
        return 0
    return n - female(male(n - 1))

i: int = 0
print(is_even(10))
print(is_odd(10))
print(is_even(7))
print(is_odd(7))
print(is_even(0))
print(is_odd(0))
print(is_even(301))
while i < 12:
    print(female(i) * 100 + male(i))
    i = i + 1
