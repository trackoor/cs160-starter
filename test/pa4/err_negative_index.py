# cpython-differs
# expect-exit: 3
# expect-stdout: 3
# expect-stdout: 30
# CPython would print 30 again for xs[-1]; ChocoPy stops with Index out of bounds.
xs: [int] = None
xs = [10, 20, 30]
print(len(xs))
print(xs[len(xs) - 1])
print(xs[-1])
print(0)
