"""Codebreaker: crack the colour code."""

import random

COLOURS = "RGBYMC"
CODE_LENGTH = 4


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


def main() -> None:
    code = make_code()
    print(f"(Psst. The code is {code}.)")
    while True:
        try:
            guess = parse_guess(input("Guess: "))
        except ValueError as error:
            print(error)
            continue
        if guess == code:
            print("Cracked it!")
            break
        print("No.")


if __name__ == "__main__":
    main()
