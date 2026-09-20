"""Dice Lab: roll a lot of dice and see what happens."""

import random
from collections import Counter
from collections.abc import Callable
from itertools import pairwise

BAR = "█"


def roll(dice: int = 2, sides: int = 6) -> list[int]:
    """Roll some dice and return a list of what each of them shows."""
    return [random.randint(1, sides) for _ in range(dice)]


def two_dice() -> int:
    """Two ordinary dice, added together."""
    return sum(roll())


def advantage() -> int:
    """Two twenty-sided dice, keeping the higher."""
    return max(roll(2, 20))


def ability_score() -> int:
    """Four dice, adding up the best three."""
    return sum(sorted(roll(4))[1:])


EXPERIMENTS: dict[str, tuple[str, Callable[[], int]]] = {
    "1": ("Two dice, added together", two_dice),
    "2": ("Two twenty-sided dice, keeping the higher", advantage),
    "3": ("Four dice, adding up the best three", ability_score),
}


def histogram(results: list[int], width: int = 50) -> list[str]:
    """Return a bar chart of how often each result came up, as a list of lines."""
    counts = Counter(results)
    biggest = max(counts.values())
    lines = []
    for value in range(min(counts), max(counts) + 1):
        count = counts[value]
        bar = BAR * round(count / biggest * width)
        lines.append(f"{value:>3} {bar} {count / len(results):.1%}")
    return lines


def average(results: list[int]) -> float:
    """Return the mean of the results."""
    return sum(results) / len(results)


def longest_streak(results: list[int]) -> tuple[int | None, int]:
    """Return the longest run of identical results, as (value, length)."""
    if not results:
        return None, 0
    best = (results[0], 1)
    length = 1
    for previous, current in pairwise(results):
        length = length + 1 if current == previous else 1
        if length > best[1]:
            best = (current, length)
    return best


def ask_for_number(prompt: str) -> int:
    """Keep asking until the user types a whole number greater than zero."""
    while True:
        reply = input(prompt)
        try:
            number = int(reply)
        except ValueError:
            print(f"{reply!r} isn't a whole number.")
            continue
        if number > 0:
            return number
        print("It needs to be more than zero.")


def main() -> None:
    print("Welcome to the Dice Lab.\n")
    for key, (description, _) in EXPERIMENTS.items():
        print(f"  {key}. {description}")

    choice = input("\nWhich experiment? ")
    while choice not in EXPERIMENTS:
        choice = input(f"Please choose from {', '.join(EXPERIMENTS)}: ")
    description, trial = EXPERIMENTS[choice]
    times = ask_for_number("How many times? ")

    results = [trial() for _ in range(times)]

    print(f"\n{description}, {times:,} times:\n")
    for line in histogram(results):
        print(line)

    value, length = longest_streak(results)
    print(f"\nAverage: {average(results):.2f}")
    print(f"Longest streak: {length} in a row, of {value}")


if __name__ == "__main__":
    main()
