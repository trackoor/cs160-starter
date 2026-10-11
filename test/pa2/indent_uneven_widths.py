# A block may be indented by any amount, and sibling blocks need not agree:
# only the stack of enclosing indentation widths matters.
x: int = 1
def f() -> int:
                return x
if x == 1:
 x = 2
 if x == 2:
          x = 3
elif x == 2:
      x = 4
else:
   x = 5
   while x > 0:
    x = x - 1
print(f())
