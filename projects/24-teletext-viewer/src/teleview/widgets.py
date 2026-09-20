"""The two parts of the screen: the line at the top, and the page."""

from collections.abc import Callable
from datetime import datetime

from pyfax import Page
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static

from teleview.glyphs import sextant
from teleview.render import page_text


class Keypad(Static):
    """The top line. It shows the page number as it's typed, and the time."""

    typed = reactive("")
    showing = reactive(100)
    now = reactive(datetime.min)  # noqa: DTZ901 - it's replaced before it's ever shown

    class Dialled(Message):
        """Sent when a whole page number has been typed."""

        def __init__(self, number: int) -> None:
            super().__init__()
            self.number = number

    def press(self, digit: str) -> None:
        """Take one digit. After the third, tell whoever is listening, and start again."""
        self.typed += digit
        if len(self.typed) == 3:
            self.post_message(self.Dialled(int(self.typed)))
            self.typed = ""

    def render(self) -> str:
        number = self.typed.ljust(3, "_") if self.typed else f"{self.showing}"
        return f"P{number}   PyFax   {self.now:%a %d %b  %H:%M:%S}"


class PageView(Static):
    """The page itself: forty columns, and the twenty-four rows under the top line."""

    page: reactive[Page | None] = reactive(None)

    def __init__(self, glyph: Callable[[int], str] = sextant) -> None:
        super().__init__()
        self.glyph = glyph

    def watch_page(self, page: Page | None) -> None:
        if page is not None:
            self.update(page_text(page, self.glyph))
