"""Turning a teletext page into something that Rich, and so Textual, can show."""

from collections.abc import Callable

from pyfax import Cell, Colour, Page
from rich.style import Style
from rich.text import Text

from teleview.glyphs import sextant

NAMES = {
    Colour.BLACK: "#000000",
    Colour.RED: "#ff0000",
    Colour.GREEN: "#00ff00",
    Colour.YELLOW: "#ffff00",
    Colour.BLUE: "#0000ff",
    Colour.MAGENTA: "#ff00ff",
    Colour.CYAN: "#00ffff",
    Colour.WHITE: "#ffffff",
}


def style_of(cell: Cell) -> Style:
    """Return a cell's colours, and, if it's a link, what clicking on it does."""
    style = Style(color=NAMES[cell.ink], bgcolor=NAMES[cell.paper], bold=True)
    if cell.link is not None:
        style += Style(underline=True, meta={"@click": f"app.go_to({cell.link})"})
    return style


def page_text(page: Page, glyph: Callable[[int], str] = sextant) -> Text:
    """Return a page as one piece of styled text: 24 lines of 40 characters.

    The page's own top line is left off, since the viewer has a live one.
    """
    text = Text(no_wrap=True)
    for number, row in enumerate(page.rows[1:]):
        if number:
            text.append("\n")
        for cell in row:
            character = glyph(cell.dots) if cell.dots else cell.text
            text.append(character, style_of(cell))
    return text
