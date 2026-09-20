"""Hi-Lo with all three Tweak challenges applied.

1. MAX_GUESSES is worked out from the range, so changing HIGHEST just works.
2. A near miss gets an encouraging "so close".
3. A guess outside the range is refused and doesn't cost a turn.
"""

import random

LOWEST = 1
HIGHEST = 1000
CLOSE = 5

# Halving the range each time, you need one guess per binary digit.
MAX_GUESSES = (HIGHEST - LOWEST + 1).bit_length()


def ask_for_number(prompt):
    """Keep asking until the player types a whole number in range."""
    while True:
        reply = input(prompt)
        try:
            number = int(reply)
        except ValueError:
            print(f"{reply!r} isn't a whole number.")
            continue
        if LOWEST <= number <= HIGHEST:
            return number
        print(f"Keep it between {LOWEST} and {HIGHEST}.")


def play_round():
    """Play one round. Return the number of guesses used, or None for a loss."""
    secret = random.randint(LOWEST, HIGHEST)
    guesses_left = MAX_GUESSES
    print(f"\nI'm thinking of a number between {LOWEST} and {HIGHEST}.")

    while guesses_left:
        guess = ask_for_number(f"[{guesses_left} left] Your guess? ")
        guesses_left -= 1
        if guess == secret:
            used = MAX_GUESSES - guesses_left
            print(f"Got it in {used} {'guess' if used == 1 else 'guesses'}!")
            return used

        hint = "Too low" if guess < secret else "Too high"
        if abs(guess - secret) <= CLOSE:
            hint += ", but so close"
        print(f"{hint}.")

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
