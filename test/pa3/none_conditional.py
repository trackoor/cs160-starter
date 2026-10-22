# Only the chosen call runs, even though neither branch produces an LLVM value.
# Expected lines: 11, 22, 11, 3. Covers expression statements and return expressions.
count: int = 0

def report(n: int):
    global count
    count = count + 1
    print(n)

def choose(flag: bool):
    return report(11) if flag else report(22)

choose(True)
choose(False)
report(11) if True else report(99)
print(count)
