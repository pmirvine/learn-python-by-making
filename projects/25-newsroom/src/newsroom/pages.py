"""Turning what was fetched into teletext pages."""

import textwrap
from datetime import date

from pyfax import COLUMNS, Colour, Page
from pyfax.content import frame

from newsroom.fetch import Result

INDEX = 100
FIRST = 101
WIDTH = COLUMNS - 4


def feed_page(number: int, result: Result, today: date, last: int) -> Page:
    """Make the page for one feed: as many headlines as there's room for."""
    before = number - 1
    after = number + 1 if number < last else None
    page = Page(number, result.feed.name, "news", before, after)
    frame(page, today, "news", Colour.RED)
    page.write(4, 1, result.feed.name[: COLUMNS - 2], Colour.YELLOW)
    if result.problem:
        page.write(6, 1, "This feed couldn't be fetched:", Colour.WHITE)
        for offset, line in enumerate(textwrap.wrap(result.problem, COLUMNS - 2)[:6]):
            page.write(8 + offset, 1, line, Colour.RED)
        return page

    row = 6
    for story in result.stories:
        lines = textwrap.wrap(story.title, WIDTH)[:3]
        if row + len(lines) > 22:
            break
        page.write(row, 1, "-", Colour.CYAN)
        for offset, line in enumerate(lines):
            page.write(row + offset, 3, line, Colour.WHITE)
        row += len(lines) + 1
    return page


def index_page(results: list[Result], today: date, note: str) -> Page:
    """Make page 100: every feed, with its page number, or with what went wrong."""
    page = Page(INDEX, "Newsroom", after=FIRST if results else None)
    frame(page, today, "news", Colour.GREEN)
    page.write(4, 1, note[: COLUMNS - 2], Colour.YELLOW)
    for offset, result in enumerate(results[:16]):
        number = FIRST + offset
        colour = Colour.RED if result.problem else Colour.WHITE
        name = result.feed.name[: COLUMNS - 12]
        count = "failed" if result.problem else f"{len(result.stories):3}"
        page.write(6 + offset, 1, f"{name:<{COLUMNS - 12}}{count:>6}", colour)
        page.write(6 + offset, COLUMNS - 4, str(number), Colour.CYAN, link=number)
    return page


def site(results: list[Result], today: date, note: str) -> list[Page]:
    """Return every page: the index, and then one for each feed."""
    last = FIRST + len(results) - 1
    pages = [index_page(results, today, note)]
    for offset, result in enumerate(results):
        pages.append(feed_page(FIRST + offset, result, today, last))
    return pages
