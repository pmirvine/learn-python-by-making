import random
from collections import Counter

TIMES = 1000
WIDTH = 50

totals = []
for _ in range(TIMES):
    total = random.randint(1, 6) + random.randint(1, 6)
    totals.append(total)

counts = Counter(totals)
biggest = max(counts.values())

for total in range(2, 13):
    count = counts[total]
    bar = "█" * round(count / biggest * WIDTH)
    print(f"{total:>3} {bar} {count / TIMES:.1%}")

value, count = counts.most_common(1)[0]
print(f"\nMost common: {value}, which came up {count} times.")
