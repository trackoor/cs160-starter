# ir-lacks: alloca
# ir-count: = phi 6
def grade(score: int) -> int:
    g: int = 0
    bonus: int = 0
    if score >= 90:
        g = 4
        bonus = 3
    elif score >= 80:
        g = 3 + bonus
    elif score >= 70:
        g = 2
        bonus = 1
    else:
        g = score - 100
    return g * 10 + bonus

print(grade(95))
print(grade(85))
print(grade(75))
print(grade(60))
print(grade(0))
