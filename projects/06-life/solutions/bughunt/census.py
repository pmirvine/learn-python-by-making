"""A population report for a pattern, with its history kept in a list."""

from collections.abc import Iterable
from itertools import islice

from life import PATTERNS, Cell, generations, parse


def chart(history: Iterable[set[Cell]], scale: int = 2) -> list[str]:
    """Return one bar for each generation, as long as its population is large."""
    return [
        f"{number:>4} {'█' * (len(universe) // scale)} {len(universe)}"
        for number, universe in enumerate(history)
    ]


def peak(history: Iterable[set[Cell]]) -> int:
    """Return the largest population there has been."""
    return max(len(universe) for universe in history)


def report(live: set[Cell], count: int) -> list[str]:
    """Chart the first `count` generations of a pattern, and then sum them up."""
    # An iterator can be gone through once. A list can be read as often as you like.
    history = list(islice(generations(live), count))
    lines = chart(history)
    lines.append(f"Peak population: {peak(history)}")
    return lines


def main() -> None:
    for line in report(parse(PATTERNS["r-pentomino"]), 40):
        print(line)


if __name__ == "__main__":
    main()
