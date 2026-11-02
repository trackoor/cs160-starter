s: str = "hello"
c: str = ""
out: str = ""
n: int = 0
for c in s:
    print(c)
for c in s:
    out = c + out
print(out)
for c in "":
    print("never")
print(c)
for c in "a" + "bc":
    n = n + len(c)
print(n)
for c in s:
    s = "xyz"
    out = out + c
print(out)
print(s)
n = 0
for c in "banana":
    if c == "a":
        n = n + 1
print(n)
