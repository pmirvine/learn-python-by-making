"""Extend 1: a prompt that remembers. Up and down go through what was typed before.

In app.py, yield a Prompt where the Input was. Nothing else changes, since a
Prompt is an Input, and query_one(Input) finds it.
"""

from typing import ClassVar

from textual.binding import Binding, BindingType
from textual.widgets import Input


class Prompt(Input):
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("up", "recall(-1)", "Earlier", show=False),
        Binding("down", "recall(1)", "Later", show=False),
    ]

    def __init__(self, placeholder: str = "", id: str | None = None) -> None:
        super().__init__(placeholder=placeholder, id=id)
        self.past: list[str] = []
        self.index = 0

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """A widget hears its own messages first, before they bubble up to the app."""
        if event.value.strip() and event.value != (self.past or [""])[-1]:
            self.past.append(event.value)
        self.index = len(self.past)

    def action_recall(self, step: int) -> None:
        self.index = max(0, min(len(self.past), self.index + step))
        self.value = self.past[self.index] if self.index < len(self.past) else ""
        self.cursor_position = len(self.value)
