import random

secret = random.randint(1, 100)
guesses = 0
print("I'm thinking of a number between 1 and 100.")

while True:
    guess = int(input("Your guess? "))
    guesses += 1

    if guess < secret:
        print("Too low.")
    elif guess > secret:
        print("Too high.")
    else:
        break

print(f"Got it in {guesses} guesses!")
