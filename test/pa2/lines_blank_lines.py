
# Blank lines produce no tokens: not at the start of the file, between
# declarations, inside a block, between a block and its else, nor at the
# end of the file. Some of them hold spaces or a tab.

x: int = 1

y: int = 2
   
def f() -> int:

    return x
        

if x == 1:

    x = 2
	
    y = 3
            
else:

    x = 4


print(x)


