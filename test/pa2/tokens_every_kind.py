# One short program with every kind of token in the subset: NAME, INTEGER,
# STRING, NEWLINE, INDENT, DEDENT, the keywords False None True and def elif
# else for global if in is not or pass return while, and the operators and
# delimiters + - * // % < > <= >= == != = ( ) [ ] , : ->
count: int = 0
items: [int] = None

def step(n: int, xs: [int]) -> int:
    global count
    if xs is None or n < 0:
        return -1
    elif not n > 10 and n != 5:
        count = count + n * 2 // 3 % 4
    else:
        pass
    for n in xs:
        count = count - n
    while count <= 0 and count >= -5:
        count = count + 1
    return count

items = [1, 2]
print(step(3, items) == 4 if True else False)
print("done")
