# Functions returning bool, used as the conditions of if, while and
# conditional expressions.
def is_prime(n: int) -> bool:
    d: int = 2
    if n < 2:
        return False
    while d * d <= n:
        if n % d == 0:
            return False
        d = d + 1
    return True

def is_even(n: int) -> bool:
    return n % 2 == 0

def both(a: bool, b: bool) -> bool:
    return a and b

n: int = 0
count: int = 0
while n < 40:
    if is_prime(n):
        print(n)
        count = count + 1
    n = n + 1
print(count)
print(is_prime(97) and not is_even(97))
print(1 if is_even(10) else 2)
print(both(is_prime(7), is_even(7)))
while not is_prime(n):
    n = n + 1
print(n)
