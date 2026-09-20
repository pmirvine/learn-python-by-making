print("Think of a number between 1 and 100. I'll guess it.")
low, high = 1, 100
tries = 0

while low <= high:
    guess = (low + high) // 2
    tries += 1
    reply = input(f"Is it {guess}? (y = yes, h = too high, l = too low) ").lower()
    if reply == "y":
        print(f"Got it in {tries}. I never need more than 7.")
        break
    elif reply == "h":
        high = guess - 1
    elif reply == "l":
        low = guess + 1
    else:
        tries -= 1
        print("Just y, h or l, please.")
else:
    print("Hmm. One of those answers was a fib.")
