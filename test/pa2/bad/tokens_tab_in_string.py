# error: 4:7
# a string holds only printable ASCII (32 to 126): line 3 escapes its tab, line 4 has a raw tab
ok: str = "a\tb"
print("a	b")
