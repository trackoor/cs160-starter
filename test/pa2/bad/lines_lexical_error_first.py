# error: 5:9
# Tokenizing the whole file finds the bad character before parsing the earlier missing operand.
x: int = 0
x =
print(x @ 2)
