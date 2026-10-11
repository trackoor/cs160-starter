# for loops over a list display, a list variable, a string literal, a string
# variable, a call, a conditional expression and a concatenation, and nested.
x: int = 0
c: str = ""
xs: [int] = None
s: str = "hello"
xss: [[int]] = None

def evens(n: int) -> [int]:
    return [0, 2, 4]

for x in [1, 2, 3]:
    print(x)
xs = [4, 5]
for x in xs:
    print(x)
for c in "abc":
    print(c)
for c in s:
    print(c)
for x in evens(3):
    print(x)
xss = [[1], [2, 3]]
for xs in xss:
    for x in xs:
        print(x)
for x in xs if len(xs) > 0 else [0]:
    print(x)
for c in s + "!":
    print(c)
