"""Codebreaker, with the challenges: no-repeat codes, classic pegs and hard mode."""

import random
from collections import Counter

from rich.console import Console

# Each peg's letter, and how Rich should paint it.
COLOURS = {
    "R": "white on red",
    "G": "black on green",
    "B": "white on blue",
    "Y": "black on yellow",
    "M": "white on magenta",
    "C": "black on cyan",
}
CODE_LENGTH = 4
MAX_TURNS = 10
REPEATS = False  # Tweak 3: may a colour appear twice in the code?
HARD_MODE = True  # Extend 2: must every guess use what you've learned?

HIT = "hit"  # the right colour, in the right place
NEAR = "near"  # the right colour, in the wrong place
MISS = "miss"

MARKS = {HIT: "[green]●[/]", NEAR: "[yellow]●[/]", MISS: "[dim]·[/]"}


def make_code(length: int = CODE_LENGTH, repeats: bool = True) -> str:
    """Return a random code. Without repeats, every peg is a different colour."""
    if repeats:
        return "".join(random.choices(list(COLOURS), k=length))
    return "".join(random.sample(list(COLOURS), k=length))


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


def pegs(code: str, guess: str) -> tuple[int, int]:
    """Score a guess as the board game does: (black pegs, white pegs).

    Black pegs count the hits. For the whites, `&` on two Counters keeps the
    smaller count of each colour, which is how many pegs the two have in
    common, wherever they are. Take away the hits, and the rest are the nears.
    """
    black = sum(wanted == got for wanted, got in zip(code, guess, strict=True))
    in_common = sum((Counter(code) & Counter(guess)).values())
    return black, in_common - black


def hard_mode_problem(history: list[tuple[str, list[str]]], guess: str) -> str | None:
    """Return what's wrong with a guess under hard mode, or None if it's allowed.

    Every hit so far must be kept, and every near colour must be used somewhere.
    """
    for earlier, marks in history:
        for position, (letter, mark) in enumerate(zip(earlier, marks, strict=True)):
            if mark == HIT and guess[position] != letter:
                return f"Peg {position + 1} must be {letter}."
            if mark == NEAR and letter not in guess:
                return f"The guess must contain {letter}."
    return None


def render_turn(guess: str, marks: list[str]) -> str:
    """Return one row of the board, in Rich's markup."""
    pegs = "".join(f"[{COLOURS[letter]}] {letter} [/]" for letter in guess)
    lights = " ".join(MARKS[mark] for mark in marks)
    return f"{pegs}  {lights}"


def render_board(history: list[tuple[str, list[str]]]) -> list[str]:
    """Return every row of the board: the turns so far, then the empty rows."""
    rows = [render_turn(guess, marks) for guess, marks in history]
    blank = "[dim]" + " · " * CODE_LENGTH + "[/]"
    return rows + [blank] * (MAX_TURNS - len(history))


def show_board(console: Console, history: list[tuple[str, list[str]]]) -> None:
    """Print the board, with a blank line above it."""
    console.print()
    for row in render_board(history):
        console.print(row)


def play_round(console: Console) -> int | None:
    """Play one game. Return the number of turns taken, or None for a loss."""
    code = make_code(repeats=REPEATS)
    history: list[tuple[str, list[str]]] = []
    solved = False

    while not solved and len(history) < MAX_TURNS:
        show_board(console, history)
        text = console.input(f"\nGuess {len(history) + 1} of {MAX_TURNS}: ")
        try:
            guess = parse_guess(text)
        except ValueError as error:
            console.print(f"[red]{error}[/]")
            continue

        problem = hard_mode_problem(history, guess) if HARD_MODE else None
        if problem:
            console.print(f"[red]Hard mode: {problem}[/]")
            continue

        marks = score(code, guess)
        black, white = pegs(code, guess)
        console.print(f"[dim]In the board game: {black} black, {white} white.[/]")
        history.append((guess, marks))
        solved = marks == [HIT] * CODE_LENGTH

    show_board(console, history)
    if solved:
        console.print(f"\n[bold green]Cracked it in {len(history)}![/]")
        return len(history)
    console.print(f"\nOut of turns. The code was {render_turn(code, [])}")
    return None


def main() -> None:
    console = Console()
    letters = " ".join(f"[{style}] {letter} [/]" for letter, style in COLOURS.items())
    console.print("[bold]Codebreaker[/]")
    console.print(f"I've made a code of {CODE_LENGTH} pegs from {letters}")
    console.print(f"{MARKS[HIT]} right colour, right place")
    console.print(f"{MARKS[NEAR]} right colour, wrong place")

    while True:
        play_round(console)
        if not console.input("\nAnother? (y/n) ").lower().startswith("y"):
            break


if __name__ == "__main__":
    main()
