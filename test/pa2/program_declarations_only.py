# A program with declarations only: global variables and functions in any
# order, and no top-level statements.
count: int = 0
name: str = "only declarations"

def bump() -> int:
    global count
    count = count + 1
    return count

limit: int = 10

def describe(n: int) -> str:
    return name
