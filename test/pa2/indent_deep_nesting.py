# Deep nesting. Inside deep, one line closes three blocks; below, print(1)
# closes five blocks at once, and the end of the file closes the last four.
n: int = 0

def deep(a: int) -> int:
    c: str = ""
    while a < 10:
        if a % 2 == 0:
            for c in "ab":
                if c == "a":
                    while a < 5:
                        a = a + 1
                    a = a + 2
        a = a + 3
    return a

print(deep(n))
if n == 0:
    if n < 1:
        if n < 2:
            if n < 3:
                if n < 4:
                    if n < 5:
                        print(n)
    print(1)
    if n < 6:
        while n < 1:
            if n == 0:
                n = n + 1
