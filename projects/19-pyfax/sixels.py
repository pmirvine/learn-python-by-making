"""All 64 of teletext's graphics characters, in order. It's counting, in binary."""

FULL, EMPTY = "██", "··"

for start in range(0, 64, 8):
    batch = range(start, start + 8)
    print("   ".join(f"{dots:06b}" for dots in batch))
    for y in range(3):
        row = []
        for dots in batch:
            left = FULL if dots >> (y * 2) & 1 else EMPTY
            right = FULL if dots >> (y * 2 + 1) & 1 else EMPTY
            row.append(f" {left}{right} ")
        print("   ".join(row))
    print()
