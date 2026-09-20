import random

TIMES = 20

totals = []
for _ in range(TIMES):
    total = random.randint(1, 6) + random.randint(1, 6)
    totals.append(total)

print(totals)
print(f"Lowest {min(totals)}, highest {max(totals)}")
print(f"Average {sum(totals) / len(totals):.2f}")
print(f"Sevens: {totals.count(7)}")
print(f"In order: {sorted(totals)}")
