NAMES = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

for row in range(6):
    for colour in range(8):
        print(f"\033[4{colour}m        ", end="")
    print("\033[0m")

for name in NAMES:
    print(f"{name:^8}", end="")
print()
