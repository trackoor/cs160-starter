# The operators again, without spaces. The lexer takes the longest operator at
# each position: <= and // are one token each, but <- is < followed by -, and
# a--b is a minus minus b.
a:int=17
b:int=5
c:bool=False
xs:[int]=None

def pick(i:int,j:int)->int:
    return i//j%2

xs=[a,b,-3]
a=a+b-a*b//a%b
a=b//-2%-3
a=-a--b
c=a<=b
c=a>=-b
c=a<-b
c=a>-b
c=a==-b
c=a!=b
c=a<b
c=a>b
a=pick(xs[0],xs[1])*-1
xs[0]=(a+b)*(a-b)
c=not(a<b)
