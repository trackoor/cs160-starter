# error: 4:8
# 2147483648 is larger than the largest literal, 2147483647, even after a unary minus
x: int = 2147483647
print(-2147483648)
