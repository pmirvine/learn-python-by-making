"""The colleague's History, mended: doing something new forgets what was undone.

    uv run solutions/bughunt/history.py

It acts out what a user reported: "I drew a red line, and undid it. I drew a blue
line down through the same place. Then I pressed Redo by mistake, and the red
line came back, across my blue one. I pressed Undo, and now there's a hole in
the blue line."
"""

import logging
import sys

from sprite_editor.commands import Command, Paint
from sprite_editor.sprite import Sprite

log = logging.getLogger("history")


class History:
    def __init__(self, sprite: Sprite) -> None:
        self.sprite = sprite
        self.done: list[Command] = []
        self.undone: list[Command] = []

    def note(self, verb: str, command: Command) -> None:
        done, undone = len(self.done), len(self.undone)
        log.debug("%s %s. %d done, %d undone", verb, command, done, undone)

    def perform(self, command: Command) -> None:
        command.do(self.sprite)
        self.done.append(command)
        self.undone.clear()
        self.note("Did", command)

    def undo(self) -> None:
        if self.done:
            command = self.done.pop()
            command.undo(self.sprite)
            self.undone.append(command)
            self.note("Undid", command)

    def redo(self) -> None:
        if self.undone:
            command = self.undone.pop()
            command.do(self.sprite)
            self.done.append(command)
            self.note("Redid", command)


def show(sprite: Sprite, caption: str) -> None:
    print(caption)
    for row in sprite.to_text().splitlines()[1:]:
        print("   ", " ".join(row))
    print()


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG, format="%(levelname)s %(message)s", stream=sys.stdout
    )
    sprite = Sprite(5, 5)
    history = History(sprite)

    history.perform(Paint("Red line", sprite, {(x, 2): 1 for x in range(5)}))
    history.undo()
    history.perform(Paint("Blue line", sprite, {(2, y): 4 for y in range(5)}))
    show(sprite, "A blue line, and nothing else:")

    history.redo()
    show(sprite, "Redo, which does nothing, since there's nothing to redo:")

    history.undo()
    show(sprite, "Undo, which takes the blue line away again:")


if __name__ == "__main__":
    main()
