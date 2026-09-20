"""The three Tweaks: a d20 experiment, a different bar, and a league table."""

import random
from collections import Counter

TIMES = 5000


def roll(dice: int = 2, sides: int = 6) -> list[int]:
    """Roll some dice and return a list of what each of them shows."""
    return [random.randint(1, sides) for _ in range(dice)]


def league_table(results: list[int], top: int = 5) -> list[str]:
    """Return the most common results, most frequent first."""
    lines = []
    for place, (value, count) in enumerate(Counter(results).most_common(top), start=1):
        lines.append(f"{place}. {value:>3} came up {count:,} times")
    return lines


def main() -> None:
    results = [sum(roll(3, 20)) for _ in range(TIMES)]
    counts = Counter(results)
    biggest = max(counts.values())
    for value in range(min(counts), max(counts) + 1):
        print(f"{value:>3} {'▒' * round(counts[value] / biggest * 60)}")
    print()
    for line in league_table(results):
        print(line)


if __name__ == "__main__":
    main()
