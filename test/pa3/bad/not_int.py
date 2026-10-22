# error: 4:14
# not needs a bool operand, but 5 is an int
ok: bool = True
print(ok and not 5)
