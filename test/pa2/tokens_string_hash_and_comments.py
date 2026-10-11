# A # inside a string literal does not start a comment; a # after the string
# does, and a comment may hold anything, even an unmatched quote.
s: str = "#"  # a comment after a string that holds a #
t: str = "# not a comment"

print("#hashtag")  # prints #hashtag
print("a # b" + t)
print("\"#\"")#a comment right after the closing parenthesis
if s == "#":  # a comment on a block header
    print("#" + "#") # "an unmatched quote in a comment
