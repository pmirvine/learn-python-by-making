"""Dice Lab: roll a lot of dice and see what happens."""

import random
from collections import Counter

BAR = "█"
TIMES = 2000


def roll(dice=2, sides=6):
    """Roll some dice and return a list of what each of them shows."""
    return [random.randint(1, sides) for _ in range(dice)]


def two_dice():
    """Two ordinary dice, added together."""
    return sum(roll())


def advantage():
    """Two twenty-sided dice, keeping the higher."""
    return max(roll(2, 20))


def ability_score():
    """Four dice, adding up the best three."""
    return sum(sorted(roll(4))[1:])


def histogram(results, width=50):
    """Return a bar chart of how often each result came up, as a list of lines."""
    counts = Counter(results)
    biggest = max(counts.values())
    lines = []
    for value in range(min(counts), max(counts) + 1):
        count = counts[value]
        bar = BAR * round(count / biggest * width)
        lines.append(f"{value:>3} {bar} {count / len(results):.1%}")
    return lines


def longest_streak(results):
    """Return the longest run of identical results, as (value, length)."""
    if not results:
        return None, 0
    best = (results[0], 1)
    length = 1
    for previous, current in zip(results, results[1:]):
        length = length + 1 if current == previous else 1
        if length > best[1]:
            best = (current, length)
    return best


def main():
    results = [ability_score() for _ in range(TIMES)]

    for line in histogram(results):
        print(line)

    print(f"\nThe first ten: {results[:10]}")
    print(f"Average: {sum(results) / len(results):.2f}")

    heroes = [score for score in results if score >= 16]
    print(f"Scores of 16 or more: {len(heroes)} ({len(heroes) / TIMES:.1%})")

    value, length = longest_streak(results)
    print(f"Longest streak: {length} in a row, of {value}")


if __name__ == "__main__":
    main()
