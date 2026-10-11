# List displays: empty, one element, several elements, nested, and with
# arbitrary expressions as elements.
xs: [int] = None
xss: [[int]] = None
bs: [bool] = None
ss: [str] = None

xs = []
xs = [1]
xs = [1, 2, 3]
print(len([[]]))
xss = [[1, 2], [3], []]
bs = [True, False, not True]
ss = ["a", "b" + "c", ""]
xs = [1 + 2, -3, len(ss), xs[0]]
xs = [1] + [2, 3] + [4]
xss = [[1], [2]] + [xs]
xss = [[1], []] if xs[0] > 0 else [[2]]
print(len([[], [[]]]))
