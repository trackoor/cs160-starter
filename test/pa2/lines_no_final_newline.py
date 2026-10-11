# This file does not end with a newline, and it ends three blocks deep: the
# lexer still ends the last line with NEWLINE and then closes all three blocks.
n: int = 3

def count(k: int) -> int:
    while k > 0:
        if k % 2 == 0:
            k = k - 1
        else:
            k = k - 2
    return k

print(count(n))
if n > 0:
    while n > 0:
        n = n - 1
        if n == 2:
            print(n)