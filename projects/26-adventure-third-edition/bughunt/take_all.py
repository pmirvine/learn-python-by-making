"""A colleague has added "take all" to the third edition. "Works on my machine."

    uv run bughunt/take_all.py

And it does work. It's F4, afterwards, that doesn't.
"""

from dataclasses import replace

from cupboard.engine import State, is_dark, things_at
from cupboard.world import ITEMS, PLAYER

from adventure.colossal import Colossal


def take_all(state: State) -> tuple[State, str]:
    """Pick up everything in the room that can be carried."""
    if is_dark(state):
        return state, "You grope about in the dark, and find nothing."
    after = replace(state, moves=state.moves + 1)
    taken = [name for name in things_at(state, state.location) if ITEMS[name].portable]
    for name in taken:
        after.places[name] = PLAYER
    return (
        after,
        f"Taken: {', '.join(taken)}." if taken else "There's nothing here to take.",
    )


class Greedy(Colossal):
    """The Colossal Cupboard, with one more command."""

    def play(self, text: str) -> str:
        if text.strip().lower() != "take all":
            return super().play(text)
        after, reply = take_all(self.state)
        self.history.append(after)
        return reply


if __name__ == "__main__":
    game = Greedy()
    for command in ["south", "east", "take all"]:
        print(">", command)
        print(game.play(command))
    print("> (F4)")
    print(game.undo())
    print("Carrying:", game.status()["Carrying"])
