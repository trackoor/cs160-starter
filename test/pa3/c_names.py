# User functions named like C functions (main, exit, puts, malloc, abort)
# and a global named printf. The runtime prints a bool with puts, so an
# unprefixed @puts would take over the runtime's calls.
printf: int = 3

def main() -> int:
    return exit(puts(printf))

def exit(code: int) -> int:
    return code * 2

def puts(n: int) -> int:
    print(n)
    return n + 1

def malloc(size: int) -> bool:
    return size > 0

def abort():
    print(0)

print(main())
print(malloc(1))
abort()
print(exit(-1))
print(malloc(0))
