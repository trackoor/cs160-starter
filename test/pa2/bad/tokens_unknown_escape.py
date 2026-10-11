# error: 4:7
# \a is not one of the four escapes, so the literal holding it is rejected at its start
s: str = "tab\there"
print("bell\a")
