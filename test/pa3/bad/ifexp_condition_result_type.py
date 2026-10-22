# error: 4:1
# The int result type is still known; the assignment precedes the bad condition.
flag: bool = False
flag = 1 if 2 else 3
