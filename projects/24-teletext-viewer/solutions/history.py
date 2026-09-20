"""Extend 1: a key that takes you back the way you came.

It's a subclass of the viewer, with a stack of page numbers.

    uv run python solutions/history.py
"""

from datetime import datetime
from pathlib import Path
from typing import ClassVar

from pyfax.content import pages
from textual.binding import Binding, BindingType

from teleview.app import Viewer


class ViewerWithBack(Viewer):
    BINDINGS: ClassVar[list[BindingType]] = [
        *Viewer.BINDINGS,
        Binding("backspace", "retrace", "Retrace"),
    ]

    def on_mount(self) -> None:
        self.trail: list[int] = []
        self.retracing = False
        super().on_mount()

    def watch_number(self, number: int) -> None:
        """Note where we've just been, unless going back is how we got here."""
        if self.is_running and not self.retracing:
            showing = self.query_one("PageView").page  # type: ignore[attr-defined]
            if showing is not None and showing.number != number:
                self.trail.append(showing.number)
        super().watch_number(number)

    def action_retrace(self) -> None:
        if self.trail:
            self.retracing = True
            self.number = self.trail.pop()
            self.retracing = False


if __name__ == "__main__":
    content = Path(__file__).parent.parent / "content"
    ViewerWithBack(pages(content, datetime.now().astimezone().date())).run()
