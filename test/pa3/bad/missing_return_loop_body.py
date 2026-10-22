# error: 3:1
# the body of the while loop always returns, but the loop may not run at all
def leading_digit(n: int) -> int:
    while n >= 10:
        return leading_digit(n // 10)

print(leading_digit(345))
