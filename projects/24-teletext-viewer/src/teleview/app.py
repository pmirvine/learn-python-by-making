"""PyFax in the terminal: a teletext viewer, with Textual."""

import argparse
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import ClassVar

from pyfax import Page
from pyfax.content import ContentError, pages
from textual import events
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Footer

from teleview.glyphs import GLYPHS, sextant
from teleview.widgets import Keypad, PageView


def local_time() -> datetime:
    return datetime.now().astimezone()


class Viewer(App[None]):
    CSS_PATH = Path(__file__).with_name("viewer.tcss")
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("left", "turn(-1)", "Back"),
        Binding("right", "turn(1)", "Next"),
        Binding("i", "go_to(100)", "Index"),
        Binding("q", "quit", "Quit"),
    ]

    number = reactive(100, init=False)

    def __init__(
        self,
        site: list[Page],
        clock: Callable[[], datetime] = local_time,
        glyph: Callable[[int], str] = sextant,
    ) -> None:
        super().__init__()
        self.site = {page.number: page for page in site}
        self.clock = clock
        self.glyph = glyph

    def compose(self) -> ComposeResult:
        with Vertical(id="set"):
            yield Keypad()
            yield PageView(self.glyph)
        yield Footer()

    def on_mount(self) -> None:
        self.tick()
        self.set_interval(1, self.tick)
        self.watch_number(self.number)

    def tick(self) -> None:
        self.query_one(Keypad).now = self.clock()

    def watch_number(self, number: int) -> None:
        """Whenever the number changes, by whatever means, show that page."""
        self.query_one(PageView).page = self.site[number]
        self.query_one(Keypad).showing = number

    def on_key(self, event: events.Key) -> None:
        if event.character and event.character.isdecimal():
            self.query_one(Keypad).press(event.character)

    def on_keypad_dialled(self, message: Keypad.Dialled) -> None:
        self.action_go_to(message.number)

    def action_go_to(self, number: int) -> None:
        if number in self.site:
            self.number = number
        else:
            self.notify(f"There's no page {number}", severity="warning")

    def action_turn(self, step: int) -> None:
        """Go to the page after this one, or the one before, if there is one."""
        page = self.site[self.number]
        wanted = page.after if step > 0 else page.before
        if wanted in self.site:
            self.number = wanted


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content", nargs="?", type=Path, default=Path("content"))
    parser.add_argument(
        "--glyphs",
        choices=sorted(GLYPHS),
        default="sextant",
        help="how to draw the graphics: try quadrant if you see empty boxes",
    )
    args = parser.parse_args()
    if not args.content.is_dir():
        raise SystemExit(
            f"Can't read the pages: there's no folder called {args.content}"
        )
    try:
        site = pages(args.content, local_time().date())
    except (OSError, ContentError) as error:
        raise SystemExit(f"Can't read the pages: {error}") from error
    Viewer(site, glyph=GLYPHS[args.glyphs]).run()
