# String literals with each of the four escapes (\" \n \t \\), the empty
# string, and every printable ASCII character. The token's value has the
# escapes applied, so "C:\\new\\table" holds backslashes, not a newline or tab.
quote: str = "\""
newline: str = "\n"
tab: str = "\t"
backslash: str = "\\"
empty: str = ""
mixed: str = "a\\b\"c\td\ne"
path: str = "C:\\new\\table"
printable: str = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"

print("say \"hi\"")
print("\\\"")
print("\\n is a backslash and an n")
print(quote + newline + tab + backslash + empty)
print("it's")
print("")
print(len(printable))
