seen: bool = False
done: bool = True
i: int = 0
while not seen:
    i = i + 1
    seen = i == 3
    done = done and i < 5
print(seen)
print(done)
print(i)
