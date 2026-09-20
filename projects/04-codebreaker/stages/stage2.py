"""Codebreaker: crack the colour code."""

import random
from collections import Counter

COLOURS = "RGBYMC"
CODE_LENGTH = 4

HIT = "hit"  # the right colour, in the right place
NEAR = "near"  # the right colour, in the wrong place
MISS = "miss"


def make_code(length: int = CODE_LENGTH) -> str:
    """Return a random code, such as "GYRG". Colours can repeat."""
    return "".join(random.choices(COLOURS, k=length))


def parse_guess(text: str) -> str:
    """Tidy up what the player typed. Raise ValueError if it can't be a guess."""
    guess = text.upper().replace(" ", "")
    if len(guess) != CODE_LENGTH:
        raise ValueError(f"A guess is {CODE_LENGTH} letters, such as RGBY.")
    strangers = set(guess) - set(COLOURS)
    if strangers:
        raise ValueError(f"I don't know {', '.join(sorted(strangers))}.")
    return guess


def score(code: str, guess: str) -> list[str]:
    """Mark each peg of the guess as a HIT, a NEAR or a MISS."""
    marks = [MISS] * len(code)
    spare: Counter[str] = Counter()

    # First pass: find the hits, and count the code's colours that weren't hit.
    for position, (wanted, got) in enumerate(zip(code, guess, strict=True)):
        if wanted == got:
            marks[position] = HIT
        else:
            spare[wanted] += 1

    # Second pass: a peg is near only while there's a spare one of its colour.
    for position, got in enumerate(guess):
        if marks[position] != HIT and spare[got] > 0:
            marks[position] = NEAR
            spare[got] -= 1

    return marks


def main() -> None:
    code = make_code()
    while True:
        try:
            guess = parse_guess(input("Guess: "))
        except ValueError as error:
            print(error)
            continue
        marks = score(code, guess)
        print("       " + " ".join(f"{mark:<4}" for mark in marks))
        if guess == code:
            print("Cracked it!")
            break


if __name__ == "__main__":
    main()
