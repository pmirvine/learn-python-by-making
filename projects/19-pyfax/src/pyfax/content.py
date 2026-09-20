"""Reading articles from TOML files, and laying them out as teletext pages."""

import re
import textwrap
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from pyfax.font import banner
from pyfax.page import COLUMNS, ROWS, Colour, Page

INDEX = 100
BODY_TOP = 6
BODY_BOTTOM = ROWS - 2
MARGIN = 1
COLOUR_CODE = re.compile(r"^\{(\w+)\}")
PAGE_NUMBER = re.compile(r"\b[1-8]\d\d\b")
SECTION_COLOURS = {"news": Colour.RED, "weather": Colour.CYAN, "fun": Colour.MAGENTA}


class ContentError(ValueError):
    """An article that can't be made into a page."""


@dataclass(frozen=True, slots=True)
class Article:
    number: int
    title: str
    section: str
    body: str
    picture: tuple[str, ...] = ()


def load(path: Path) -> Article:
    """Read one article from a TOML file."""
    with path.open("rb") as file:
        data = tomllib.load(file)
    match data:
        case {"number": int(number), "title": str(title), "body": str(body)}:
            pass
        case _:
            raise ContentError(f"{path.name} needs a number, a title and a body")
    if not INDEX < number < 900:
        raise ContentError(f"{path.name}: page numbers go from 101 to 899")
    picture = data.get("picture", "")
    return Article(
        number,
        title,
        str(data.get("section", "news")),
        body,
        tuple(str(picture).strip().splitlines()),
    )


def load_all(folder: Path) -> list[Article]:
    """Read every article in a folder, in order of page number."""
    articles = sorted(
        (load(path) for path in folder.glob("*.toml")), key=lambda a: a.number
    )
    numbers = [article.number for article in articles]
    for number in numbers:
        if numbers.count(number) > 1:
            raise ContentError(f"There are two pages numbered {number}")
    return articles


def frame(page: Page, today: date, heading: str, colour: Colour) -> None:
    """Draw what every page has: the top line, a banner, and the links at the bottom."""
    page.write(0, 0, f"P{page.number}", Colour.WHITE)
    page.write(0, 7, "PyFax", Colour.YELLOW)
    page.write(0, COLUMNS - 11, f"{today:%a %d %b}", Colour.CYAN)
    page.picture(1, MARGIN, banner(heading), colour)

    page.write(ROWS - 1, 1, "Index 100", Colour.RED, link=INDEX)
    if page.before is not None:
        page.write(ROWS - 1, 14, f"Back {page.before}", Colour.GREEN, link=page.before)
    if page.after is not None:
        page.write(ROWS - 1, 27, f"Next {page.after}", Colour.CYAN, link=page.after)


def lines_of(body: str) -> list[tuple[str, Colour]]:
    """Split an article into lines that fit, each with its colour.

    A line that begins with a colour in curly brackets, such as {yellow}, is kept
    as one line, in that colour. Everything else is a paragraph, to be wrapped.
    """
    lines: list[tuple[str, Colour]] = []
    for paragraph in body.strip().split("\n\n"):
        text = " ".join(paragraph.split())
        colour = Colour.WHITE
        if found := COLOUR_CODE.match(text):
            name = found[1].upper()
            if name not in Colour.__members__:
                raise ContentError(f"There's no such colour as {found[1]}")
            colour = Colour[name]
            text = text[found.end() :]
        wrapped = textwrap.wrap(text, COLUMNS - 2 * MARGIN) or [""]
        lines += [(line, colour) for line in wrapped]
        lines.append(("", Colour.WHITE))
    return lines[:-1]


def write_linked(page: Page, row: int, text: str, ink: Colour, known: set[int]) -> None:
    """Write a line, and make a link of every number in it that's a page we have."""
    page.write(row, MARGIN, text, ink)
    for found in PAGE_NUMBER.finditer(text):
        number = int(found.group())
        if number in known:
            column = MARGIN + found.start()
            page.write(row, column, found.group(), Colour.CYAN, link=number)


def neighbours(number: int, known: set[int]) -> tuple[int | None, int | None]:
    """Return the numbers of the pages before and after this one, if there are any."""
    earlier = [other for other in known if other < number]
    later = [other for other in known if other > number]
    return max(earlier, default=None), min(later, default=None)


def lay_out(article: Article, known: set[int], today: date) -> Page:
    """Make the page for an article."""
    before, after = neighbours(article.number, known)
    page = Page(article.number, article.title, article.section, before, after)
    colour = SECTION_COLOURS.get(article.section, Colour.GREEN)
    frame(page, today, article.section, colour)
    page.write(4, MARGIN, article.title[: COLUMNS - 2], Colour.YELLOW)

    row = BODY_TOP
    if article.picture:
        page.picture(row, MARGIN, list(article.picture), colour)
        row += -(-len(article.picture) // 3) + 1
    lines = lines_of(article.body)
    if row + len(lines) > BODY_BOTTOM + 1:
        extra = row + len(lines) - BODY_BOTTOM - 1
        raise ContentError(f"Page {article.number} is {extra} lines too long")
    for offset, (text, ink) in enumerate(lines):
        write_linked(page, row + offset, text, ink, known)
    return page


def index(articles: list[Article], today: date) -> Page:
    """Make page 100, which lists all the others."""
    first = min((article.number for article in articles), default=None)
    page = Page(INDEX, "Index", after=first)
    frame(page, today, "PyFax", Colour.GREEN)
    row = 4
    for section in dict.fromkeys(article.section for article in articles):
        colour = SECTION_COLOURS.get(section, Colour.GREEN)
        page.write(row, MARGIN, section.upper(), colour)
        row += 1
        for article in articles:
            if article.section == section and row < BODY_BOTTOM:
                number = article.number
                title = article.title[: COLUMNS - 8]
                dots = "." * (COLUMNS - 2 * MARGIN - len(title) - 3)
                page.write(row, MARGIN, title + dots, Colour.WHITE)
                page.write(row, COLUMNS - 4, str(number), Colour.CYAN, link=number)
                row += 1
        row += 1
    return page


def pages(folder: Path, today: date) -> list[Page]:
    """Return every page of the site: the index, and then the articles."""
    articles = load_all(folder)
    known = {INDEX} | {article.number for article in articles}
    return [index(articles, today)] + [lay_out(a, known, today) for a in articles]
