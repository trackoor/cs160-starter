text: str = "the quick brown fox jumps over the lazy dog"
alphabet: str = "abcdefghijklmnopqrstuvwxyz"
letters: [int] = None
i: int = 0

def count(s: str, c: str) -> int:
    n: int = 0
    ch: str = ""
    for ch in s:
        if ch == c:
            n = n + 1
    return n

def count_vowels(s: str) -> int:
    n: int = 0
    v: str = ""
    for v in "aeiou":
        n = n + count(s, v)
    return n

print(count(text, "o"))
print(count(text, " "))
print(count(text, "z"))
print(count("", "a"))
print(count_vowels(text))
letters = []
while i < len(alphabet):
    letters = letters + [count(text, alphabet[i])]
    i = i + 1
print(len(letters))
i = 0
while i < len(letters):
    if letters[i] > 1:
        print(alphabet[i])
        print(letters[i])
    i = i + 1
