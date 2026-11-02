a: [[int]] = None
b: [[int]] = None
c: [int] = None
d: [int] = None
e: [int] = None
s: str = "ab"
t: str = ""
a = [[1], [2]]
b = a + [[3]]
b[0][0] = 9
print(a[0][0])
print(len(b))
b[1] = [20, 21]
print(a[1][0])
print(b[1][1])
print(a[0] is b[0])
print(a[1] is b[1])
print(a is b)
c = [1, 2, 3]
e = []
d = c + e
d[0] = 100
print(c[0])
print(d[0])
print(c is d)
d = e + c
print(d is c)
print(len(c + d + c))
t = s + ""
print(t == s)
t = t + "c"
print(s)
print(t)
