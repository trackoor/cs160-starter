# Towers of Hanoi: a recursive function without a return type whose
# recursive calls permute its arguments. Each move prints disk, from, to.
moves: int = 0
verbose: bool = True

def move(disk: int, src: int, dst: int):
    global moves
    moves = moves + 1
    if verbose:
        print(disk * 100 + src * 10 + dst)

def hanoi(n: int, src: int, dst: int, via: int):
    if n == 0:
        return
    hanoi(n - 1, src, via, dst)
    move(n, src, dst)
    hanoi(n - 1, via, dst, src)

hanoi(3, 1, 3, 2)
print(moves)
verbose = False
moves = 0
hanoi(10, 1, 3, 2)
print(moves)
