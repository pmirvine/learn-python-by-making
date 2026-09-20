import random

secret = random.randint(1, 100)
print("I'm thinking of a number between 1 and 100.")

guess = int(input("Your guess? "))

if guess < secret:
    print("Too low.")
elif guess > secret:
    print("Too high.")
else:
    print("Got it!")

print(f"The number was {secret}.")
