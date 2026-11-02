# error: 4:5
# Iterating over a str gives str elements, but c is declared int.
c: int = 0
for c in "abc":
    print(c)
