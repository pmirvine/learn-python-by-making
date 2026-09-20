"""The letters pages: what readers have written, and the rules for writing in."""

import textwrap
from datetime import date

from pyfax import COLUMNS, Colour, Page
from pyfax.content import frame

from pyfax_live.db import Letter

NUMBER = 500
FORM = 599
LONGEST_NAME = 20
LONGEST_MESSAGE = 200


def check(name: str, message: str) -> list[str]:
    """Return what's wrong with a letter, as a list of complaints. None is good news."""
    problems: list[str] = []
    if not name:
        problems.append("Please say who you are.")
    elif len(name) > LONGEST_NAME:
        problems.append(f"That name is too long: {LONGEST_NAME} letters at most.")
    if not message:
        problems.append("Your letter is empty.")
    elif len(message) > LONGEST_MESSAGE:
        problems.append(f"Too long: {LONGEST_MESSAGE} letters at most.")
    if not (name + message).isprintable():
        problems.append("There's something in there that can't be printed.")
    return problems


def page(letters: list[Letter], today: date, notice: str = "") -> Page:
    """Make page 500, with as many of the latest letters as there's room for."""
    sheet = Page(NUMBER, "Your letters", "letters", before=301, after=FORM)
    frame(sheet, today, "letters", Colour.MAGENTA)
    sheet.write(4, 1, f"To write to us, go to page {FORM}", Colour.YELLOW)
    sheet.write(4, 29, str(FORM), Colour.CYAN, link=FORM)
    if notice:
        sheet.write(5, 1, notice[: COLUMNS - 2], Colour.GREEN)

    row = 7
    for letter in letters:
        lines = textwrap.wrap(letter.message, COLUMNS - 4)
        if row + len(lines) + 1 > 22:
            break
        sheet.write(row, 1, f"{letter.name} writes:", Colour.CYAN)
        for offset, line in enumerate(lines, start=1):
            sheet.write(row + offset, 3, line, Colour.WHITE)
        row += len(lines) + 2
    if not letters:
        sheet.write(row, 1, "Nobody has written in yet.", Colour.WHITE)
    return sheet
