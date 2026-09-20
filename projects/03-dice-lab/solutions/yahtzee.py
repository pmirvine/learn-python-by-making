"""Extend 1: how often do five dice show at least three of a kind?"""

import random
from collections import Counter

TIMES = 20_000


def roll(dice: int = 2, sides: int = 6) -> list[int]:
    """Roll some dice and return a list of what each of them shows."""
    return [random.randint(1, sides) for _ in range(dice)]


def best_group(dice: list[int]) -> int:
    """Return the size of the largest group of matching dice."""
    return max(Counter(dice).values())


def main() -> None:
    groups = Counter(best_group(roll(5)) for _ in range(TIMES))
    for size in range(1, 6):
        print(f"Best group of {size}: {groups[size] / TIMES:6.2%}")
    at_least_three = sum(count for size, count in groups.items() if size >= 3)
    print(f"\nThree of a kind or better: {at_least_three / TIMES:.1%}")


if __name__ == "__main__":
    main()
