# ir-lacks: alloca
def weigh(xs: [int], s: str) -> int:
    x: int = 0
    c: str = "-"
    n: int = 0
    for x in xs:
        for c in s:
            if c == "a":
                n = n + x
    print(c)
    return n * 100 + x

def join_all(words: [str]) -> str:
    w: str = ""
    out: str = ""
    for w in words:
        out = out + w + ","
    return out

print(weigh([1, 2, 3], "banana"))
print(weigh([], "abc"))
print(weigh([4, 5], ""))
print(join_all(["x", "yy", "zzz"]))
print(join_all([]))
