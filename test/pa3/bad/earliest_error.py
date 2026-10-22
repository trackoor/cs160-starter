# error: 5:12
# Two errors: count + flag in total (line 5) and the initial value of limit (line 8).
# A checker may find the second one first, but it must report the one that comes first in the file.
def total(count: int) -> int:
    return count + flag

flag: bool = True
limit: int = False
print(total(1))
