from datetime import date
from html.parser import HTMLParser
from pathlib import Path

import pytest

from pyfax import COLUMNS, ROWS, Cell, Colour
from pyfax.build import classes, stylesheet, write_site
from pyfax.content import pages

CONTENT = Path(__file__).parent.parent / "content"


class Census(HTMLParser):
    """Count the cells on a page, and collect its links and its text."""

    def __init__(self) -> None:
        super().__init__()
        self.cells = 0
        self.rows = 0
        self.links: set[str] = set()
        self.text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "div" and attributes.get("class") == "row":
            self.rows += 1
        if tag in ("span", "a") and "class" in attributes:
            self.cells += 1
        if tag == "a" and attributes.get("href"):
            self.links.add(str(attributes["href"]))

    def handle_data(self, data: str) -> None:
        self.text += data


@pytest.fixture(scope="module")
def site(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("site")
    write_site(pages(CONTENT, date(2026, 9, 20)), out)
    return out


def census(path: Path) -> Census:
    counter = Census()
    counter.feed(path.read_text(encoding="utf-8"))
    return counter


def test_classes():
    assert classes(Cell()) == "i7 p0"
    assert classes(Cell(ink=Colour.RED, paper=Colour.BLUE, dots=21)) == "i1 p4 m m21"
    assert classes(Cell(dots=0)) == "i7 p0"


def test_every_page_is_a_full_screen(site):
    written = sorted(site.glob("[1-9]*.html"))
    assert [path.stem for path in written] == ["100", "101", "102", "301", "404", "501"]
    for path in written:
        counted = census(path)
        assert (counted.rows, counted.cells) == (ROWS, ROWS * COLUMNS), path.name


def test_every_link_leads_somewhere(site):
    for path in site.glob("*.html"):
        for link in census(path).links:
            assert (site / link).is_file(), f"{path.name} links to {link}"


def test_awkward_characters_are_escaped_by_the_template(site):
    html = (site / "101.html").read_text(encoding="utf-8")
    assert '<span class="i7 p0">&amp;</span>' in html
    assert '<span class="i6 p0">&#34;</span>' in html
    assert "fair's fair & it was" in " ".join(census(site / "101.html").text.split())


def test_the_home_page_is_the_index(site):
    index = (site / "index.html").read_text(encoding="utf-8")
    assert index == (site / "100.html").read_text(encoding="utf-8")


def test_the_stylesheet_has_the_colours_and_the_graphics_added(site):
    css = (site / "style.css").read_text(encoding="utf-8")
    assert css == stylesheet()
    assert ".i3 { color: #ff0; }" in css
    assert ".p4 { background-color: #00f; }" in css
    assert css.count("\n.m") >= 63
    assert "display: contents" in css
