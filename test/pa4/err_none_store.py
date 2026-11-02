# expect-exit: 4
xss: [[int]] = None
xss = [None, [1]]
print(xss[1][0])
xss[1][0] = 2
print(xss[1][0])
xss[0][0] = 3
print(4)
