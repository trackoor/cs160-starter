# Comment-only lines produce no tokens, whatever their indentation: they
# neither open nor close a block.
x: int = 0
        # a comment indented deeper than anything around it
def f(n: int) -> int:
# a comment at column 0 inside the function
    # a comment at the body's indentation
            # a comment deeper than the body
    if n > 0:
  # a comment between two indentation levels
        return n
    # a comment before the dedent
    return 0
    # a comment after the last statement of the body
if x == 0:
    x = f(1)
        # a comment deeper than the block
# a comment between the if block and its else
else:
    x = 2
    # a comment at the block's indentation, just before the block ends
#
#no space after the hash; the next line is a commented-out block header
    #if x == 0:
print(x)
