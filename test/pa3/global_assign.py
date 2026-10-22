# A function may read a global freely, but assigns to it only after `global`.
count: int = 0
total: int = 100
done: bool = False

def bump(n: int) -> int:
    global count
    count = count + n
    return count

def peek() -> int:
    count: int = 100
    return count

def read_count() -> int:
    return count

def finish():
    global done
    global total
    total = total - count
    done = True

print(bump(5))
print(peek())
print(count)
print(bump(3))
print(read_count())
print(done)
finish()
print(done)
print(total)
count = 1
print(read_count())
print(bump(1))
print(count)
