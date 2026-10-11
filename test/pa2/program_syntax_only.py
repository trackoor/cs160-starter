# PA2 checks syntax and tree shape: these expressions need not type-check or run.
# Catch a parser that tries to enforce declaration lookup or int/bool type rules.
count: int = True

print(unknown)
count = 1 + True
print(not 5)
