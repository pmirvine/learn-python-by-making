import random

LOWEST = 1
HIGHEST = 100
MAX_GUESSES = 7

secret = random.randint(LOWEST, HIGHEST)
guesses_left = MAX_GUESSES
print(f"I'm thinking of a number between {LOWEST} and {HIGHEST}.")
print(f"You have {MAX_GUESSES} guesses.")

while guesses_left:
    reply = input(f"[{guesses_left} left] Your guess? ")
    try:
        guess = int(reply)
    except ValueError:
        print(f"{reply!r} isn't a whole number.")
        continue

    guesses_left -= 1
    if guess < secret:
        print("Too low.")
    elif guess > secret:
        print("Too high.")
    else:
        used = MAX_GUESSES - guesses_left
        print(f"Got it in {used} {'guess' if used == 1 else 'guesses'}!")
        break
else:
    print(f"Out of guesses. I was thinking of {secret}.")
