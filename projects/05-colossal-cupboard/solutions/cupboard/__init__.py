"""The Colossal Cupboard: a small text adventure."""

import textwrap
from pathlib import Path

from cupboard.engine import State, describe, respond
from cupboard.saves import SaveError, load, save

SAVE_FILE = Path("cupboard-save.json")


def show(text: str) -> None:
    """Print a reply, wrapping long lines but keeping indented ones as they are."""
    for line in text.splitlines():
        print(line if line.startswith(" ") else textwrap.fill(line, width=72))


def main() -> None:
    state = State()
    # Every state the game has been in. respond() never changes a state, so
    # keeping the old ones costs nothing, and undo is just a step backwards.
    history: list[State] = []
    show(describe(state))

    while not state.won:
        text = input("\n> ")
        match text.strip().lower():
            case "quit" | "q":
                break
            case "undo":
                if history:
                    state = history.pop()
                    show("Undone.\n" + describe(state))
                else:
                    show("There's nothing to undo.")
            case "save":
                try:
                    save(state, SAVE_FILE)
                    show("Saved.")
                except SaveError as error:
                    show(str(error))
            case "restore":
                try:
                    state = load(SAVE_FILE)
                    show("Restored.\n" + describe(state))
                except SaveError as error:
                    show(str(error))
            case _:
                new, reply = respond(state, text)
                if new != state:
                    history.append(state)
                state = new
                show(reply)

    show("Bye.")
