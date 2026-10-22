# scaled reads three globals without declaring them; each call sees
# the values they hold at that moment.
base: int = 10
scale: int = 2
enabled: bool = True

def scaled(n: int) -> int:
    if enabled:
        return n * scale + base
    return n

def set_scale(s: int):
    global scale
    scale = s

print(scaled(5))
base = 100
print(scaled(5))
set_scale(7)
print(scaled(5))
enabled = False
print(scaled(5))
print(scale)
