"""Hi-Lo with both Extend challenges: a difficulty menu and session statistics."""

import random

LOWEST = 1


def ask_for_number(prompt, lowest, highest):
    """Keep asking until the player types a whole number from lowest to highest."""
    while True:
        reply = input(prompt)
        try:
            number = int(reply)
        except ValueError:
            print(f"{reply!r} isn't a whole number.")
            continue
        if lowest <= number <= highest:
            return number
        print(f"Keep it between {lowest} and {highest}.")


def choose_highest():
    """Show the difficulty menu and return the top of the chosen range."""
    print("\n1. Easy    (1 to 10)")
    print("2. Normal  (1 to 100)")
    print("3. Fiendish (1 to 10,000)")
    choice = ask_for_number("Difficulty? ", 1, 3)
    if choice == 1:
        return 10
    elif choice == 2:
        return 100
    return 10_000


def play_round(highest):
    """Play one round. Return the number of guesses used, or None for a loss."""
    secret = random.randint(LOWEST, highest)
    max_guesses = (highest - LOWEST + 1).bit_length()
    guesses_left = max_guesses
    print(f"I'm thinking of a number between {LOWEST} and {highest:,}.")

    while guesses_left:
        prompt = f"[{guesses_left} left] Your guess? "
        guess = ask_for_number(prompt, LOWEST, highest)
        guesses_left -= 1
        if guess < secret:
            print("Too low.")
        elif guess > secret:
            print("Too high.")
        else:
            used = max_guesses - guesses_left
            print(f"Got it in {used} {'guess' if used == 1 else 'guesses'}!")
            return used

    print(f"Out of guesses. I was thinking of {secret:,}.")
    return None


def main():
    rounds = 0
    wins = 0
    total_guesses = 0

    while True:
        score = play_round(choose_highest())
        rounds += 1
        if score is not None:
            wins += 1
            total_guesses += score
        if not input("Play again? (y/n) ").lower().startswith("y"):
            break

    print(f"\nYou won {wins} of {rounds} {'round' if rounds == 1 else 'rounds'}.")
    if wins:
        print(f"Average guesses per win: {total_guesses / wins:.1f}")


if __name__ == "__main__":
    main()
