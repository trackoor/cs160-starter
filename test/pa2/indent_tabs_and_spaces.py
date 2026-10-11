# Tabs and spaces mixed in indentation (consistently, as Python requires): a
# tab then four spaces is width 12, tab + 4 spaces + tab is width 16, and four
# spaces then a tab is width 8. Columns still count characters.
x: int = 0
if x == 0:
	x = 1
	if x == 1:
	    x = 2
	    while x > 0:
	    	x = x - 1
	    print(x)
	print(x)
while x < 2:
    x = x + 1
    if x == 1:
    	print(x)
    print(x)
