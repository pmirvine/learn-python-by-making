"""Hi-Lo: I think of a number, you guess it."""

import random

LOWEST = 1
HIGHEST = 100
MAX_GUESSES = 7


def ask_for_number(prompt):
    """Keep asking until the player types a whole number, then return it."""
    while True:
        reply = input(prompt)
        try:
            return int(reply)
        except ValueError:
            print(f"{reply!r} isn't a whole number.")


def play_round():
    """Play one round. Return the number of guesses used, or None for a loss."""
    secret = random.randint(LOWEST, HIGHEST)
    guesses_left = MAX_GUESSES
    print(f"\nI'm thinking of a number between {LOWEST} and {HIGHEST}.")

    while guesses_left:
        guess = ask_for_number(f"[{guesses_left} left] Your guess? ")
        guesses_left -= 1
        if guess < secret:
            print("Too low.")
        elif guess > secret:
            print("Too high.")
        else:
            used = MAX_GUESSES - guesses_left
            print(f"Got it in {used} {'guess' if used == 1 else 'guesses'}!")
            return used

    print(f"Out of guesses. I was thinking of {secret}.")
    return None


def main():
    best = None
    while True:
        score = play_round()
        if score is not None and (best is None or score < best):
            best = score
            print(f"That's a new best: {best}.")
        if not input("Play again? (y/n) ").lower().startswith("y"):
            break

    if best is None:
        print("Thanks for playing.")
    else:
        print(f"Thanks for playing. Your best was {best}.")


if __name__ == "__main__":
    main()
