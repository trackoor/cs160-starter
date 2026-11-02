def reverse(s: str) -> str:
    out: str = ""
    i: int = 0
    i = len(s) - 1
    while i >= 0:
        out = out + s[i]
        i = i - 1
    return out

def reverse_for(s: str) -> str:
    out: str = ""
    c: str = ""
    for c in s:
        out = c + out
    return out

def is_palindrome(s: str) -> bool:
    return s == reverse(s)

print(reverse("stressed"))
print(reverse_for("drawer"))
print(reverse(""))
print(len(reverse("")))
print(reverse("a"))
print(is_palindrome("racecar"))
print(is_palindrome("chocopy"))
print(reverse(reverse("round trip")) == "round trip")
print(reverse("tab\tnew\nline") == reverse_for("tab\tnew\nline"))
print(reverse("tab\tnew\nline"))
