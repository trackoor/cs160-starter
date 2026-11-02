s: str = "tab\there"
t: str = "line1\nline2"
q: str = "say \"hi\""
b: str = "back\\slash"
print(s)
print(t)
print(q)
print(b)
print(len(s))
print(len(t))
print(len(q))
print(len(b))
print(t[5] == "\n")
print(q[4])
print(b[4])
print("\"" + "\\" + "\"")
print("a\n\nb")
print("")
print("# not a comment")
print(len("\t\n\\\""))
