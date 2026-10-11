# Indentation with tabs: a tab advances to the next multiple of 8. Columns
# count characters, so a statement after one tab has col_offset 1. Tabs also
# separate tokens within a line.
x:	int	=	0

def f(n:	int)	->	int:
	if n > 0:
		return	n
	return 0

while x < 3:
	x = x + 1
	if x == 2:
		print(f(x))
	else:
		print(x)
print(x)
