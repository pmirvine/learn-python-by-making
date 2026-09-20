import sys

RULE = int(sys.argv[1]) if len(sys.argv) > 1 else 90
WIDTH = 79


def rows(rule, width):
    cells = [0] * width
    cells[width // 2] = 1
    while True:
        yield cells
        cells = [
            rule >> (4 * cells[i - 1] + 2 * cells[i] + cells[(i + 1) % width]) & 1
            for i in range(width)
        ]


for number, row in enumerate(rows(RULE, WIDTH)):
    print("".join("█" if cell else " " for cell in row))
    if number == 39:
        break
