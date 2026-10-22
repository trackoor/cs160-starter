# error: 7:12
# inside run, total is an int parameter that shadows the function total
def total(n: int) -> int:
    return n + 1

def run(total: int) -> int:
    return total(3)

print(run(1))
