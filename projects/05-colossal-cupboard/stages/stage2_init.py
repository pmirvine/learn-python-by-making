"""The Colossal Cupboard: a small text adventure."""

import textwrap

from cupboard.engine import State, describe, respond


def show(text: str) -> None:
    """Print a reply, wrapping long lines but keeping indented ones as they are."""
    for line in text.splitlines():
        print(line if line.startswith(" ") else textwrap.fill(line, width=72))


def main() -> None:
    state = State()
    show(describe(state))

    while not state.won:
        text = input("\n> ")
        if text.strip().lower() in ("quit", "q"):
            break
        state, reply = respond(state, text)
        show(reply)

    show("Bye.")
