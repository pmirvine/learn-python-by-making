"""Codebreaker, with a board that a colleague 'tidied up'. Something's wrong with it."""

import random
from collections import Counter

COLOURS = "RGBYMC"
CODE_LENGTH = 4
MAX_TURNS = 10

HIT = "hit"
NEAR = "near"
MISS = "miss"
LIGHTS = {HIT: "●", NEAR: "○", MISS: "·"}

# Build the empty board once, and copy it for each game. Much more efficient!
EMPTY_ROW = ["·"] * CODE_LENGTH
EMPTY_BOARD = [EMPTY_ROW] * MAX_TURNS


def new_board() -> list[list[str]]:
    """Return an empty board: MAX_TURNS rows of CODE_LENGTH cells."""
    return EMPTY_BOARD.copy()


def place(board: list[list[str]], turn: int, guess: str) -> None:
    """Put the pegs of a guess into one row of the board."""
    for position, letter in enumerate(guess):
        board[turn][position] = letter


def render(board: list[list[str]]) -> list[str]:
    """Return the board as lines of text."""
    return [" ".join(row) for row in board]


def make_code(length: int = CODE_LENGTH) -> str:
    return "".join(random.choices(COLOURS, k=length))


def parse_guess(text: str) -> str:
    guess = text.upper().replace(" ", "")
    if len(guess) != CODE_LENGTH:
        raise ValueError(f"A guess is {CODE_LENGTH} letters, such as RGBY.")
    strangers = set(guess) - set(COLOURS)
    if strangers:
        raise ValueError(f"I don't know {', '.join(sorted(strangers))}.")
    return guess


def score(code: str, guess: str) -> list[str]:
    marks = [MISS] * len(code)
    spare: Counter[str] = Counter()
    for position, (wanted, got) in enumerate(zip(code, guess, strict=True)):
        if wanted == got:
            marks[position] = HIT
        else:
            spare[wanted] += 1
    for position, got in enumerate(guess):
        if marks[position] != HIT and spare[got] > 0:
            marks[position] = NEAR
            spare[got] -= 1
    return marks


def play_round() -> None:
    code = make_code()
    board = new_board()
    turn = 0
    while turn < MAX_TURNS:
        print()
        for line in render(board):
            print(line)
        try:
            guess = parse_guess(input(f"\nGuess {turn + 1} of {MAX_TURNS}: "))
        except ValueError as error:
            print(error)
            continue
        place(board, turn, guess)
        marks = score(code, guess)
        print(" ".join(LIGHTS[mark] for mark in marks))
        if guess == code:
            print("Cracked it!")
            return
        turn += 1
    print(f"Out of turns. The code was {code}.")


def main() -> None:
    while True:
        play_round()
        if not input("\nAnother? (y/n) ").lower().startswith("y"):
            break


if __name__ == "__main__":
    main()
