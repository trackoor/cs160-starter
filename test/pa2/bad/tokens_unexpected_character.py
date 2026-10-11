# error: 4:7
# ! is not a token on its own (only as part of !=), so the lexer rejects it
b: bool = True
print(!b)
