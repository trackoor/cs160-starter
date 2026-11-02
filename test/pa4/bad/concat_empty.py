# error: 4:6
# [] has type <Empty>, which is not a list type [T], so it cannot be an operand of +
xs: [int] = None
xs = [] + [1]
print(len(xs))
