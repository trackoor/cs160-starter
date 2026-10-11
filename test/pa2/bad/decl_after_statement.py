# error: 5:2
# declarations come before the first statement, so after print(x) the : is unexpected
x: int = 0
print(x)
y: int = 1
