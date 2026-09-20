import random
from collections import Counter

ROWS = 12
BALLS = 2000
HEIGHT = 16

bins = Counter(sum(random.choice((0, 1)) for _ in range(ROWS)) for _ in range(BALLS))
tallest = max(bins.values())

for level in range(HEIGHT, 0, -1):
    row = ""
    for position in range(ROWS + 1):
        row += " █ " if bins[position] / tallest * HEIGHT >= level else "   "
    print(row)

print("".join(f"{position:^3}" for position in range(ROWS + 1)))
