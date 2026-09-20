"""Extend 2: which is better, two six-sided dice or one twelve-sided die?"""

import random

TIMES = 20_000


def roll(dice: int = 2, sides: int = 6) -> list[int]:
    """Roll some dice and return a list of what each of them shows."""
    return [random.randint(1, sides) for _ in range(dice)]


def wins(first: list[int], second: list[int]) -> tuple[int, int, int]:
    """Compare two players' results round by round: (first wins, draws, second wins)."""
    pairs = list(zip(first, second, strict=True))
    first_wins = sum(a > b for a, b in pairs)
    draws = sum(a == b for a, b in pairs)
    return first_wins, draws, len(pairs) - first_wins - draws


def main() -> None:
    two_d6 = [sum(roll(2, 6)) for _ in range(TIMES)]
    one_d12 = [sum(roll(1, 12)) for _ in range(TIMES)]
    first, draws, second = wins(two_d6, one_d12)
    print(f"Two d6 win {first / TIMES:.1%}, one d12 wins {second / TIMES:.1%}")
    print(f"and {draws / TIMES:.1%} are draws.")


if __name__ == "__main__":
    main()
