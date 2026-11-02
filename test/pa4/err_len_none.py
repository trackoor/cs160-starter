# expect-exit: 1
words: [str] = None
n: int = 0
words = ["a", "bc"]
n = len(words) + len(words[1])
print(n)
words = None
print(len("still fine"))
n = len(words)
print(n)
