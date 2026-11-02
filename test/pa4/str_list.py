words: [str] = None
w: str = ""
sentence: str = ""
first: bool = True

def index_of(ws: [str], target: str) -> int:
    i: int = 0
    while i < len(ws):
        if ws[i] == target:
            return i
        i = i + 1
    return -1

words = ["compilers", "are", "fun"]
print(words[0])
print(len(words))
print(len(words[0]))
words[2] = "great"
for w in words:
    if first:
        sentence = w
        first = False
    else:
        sentence = sentence + " " + w
print(sentence)
print(len(sentence))
print(words[1][0] + words[2][4])
words = words + ["!"]
print(words[3])
print(words[0][len(words[0]) - 1])
print(index_of(words, "are"))
print(index_of(words, "fun"))
print(index_of(words, "!"))
print(index_of([], "x"))
