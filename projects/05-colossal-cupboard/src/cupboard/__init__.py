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
    show(describe(state))

    while not state.won:
        text = input("\n> ")
        match text.strip().lower():
            case "quit" | "q":
                break
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
                state, reply = respond(state, text)
                show(reply)

    show("Bye.")
