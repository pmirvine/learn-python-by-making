STEPS = 11_000

black = set()
x, y = 0, 0
dx, dy = 0, -1

for _ in range(STEPS):
    if (x, y) in black:
        black.remove((x, y))
        dx, dy = dy, -dx
    else:
        black.add((x, y))
        dx, dy = -dy, dx
    x, y = x + dx, y + dy

columns = [x for x, _ in black]
rows = [y for _, y in black]
for row in range(min(rows), max(rows) + 1):
    line = ""
    for column in range(min(columns), max(columns) + 1):
        line += "█" if (column, row) in black else " "
    print(line)
