from datetime import date
from pathlib import Path

import pytest

from pyfax import COLUMNS, Colour
from pyfax.content import ContentError, lines_of, load, load_all, neighbours, pages

TODAY = date(2026, 9, 20)
GOOD = 'number = 101\ntitle = "Hello"\nbody = """\n{yellow}Big news\n\nSee 102 & 999.\n"""\n'


def write(folder: Path, name: str, text: str) -> Path:
    path = folder / name
    path.write_text(text, encoding="utf-8")
    return path


def test_loading_an_article(tmp_path):
    article = load(write(tmp_path, "a.toml", GOOD))
    assert (article.number, article.title, article.section) == (101, "Hello", "news")


@pytest.mark.parametrize(
    ("text", "complaint"),
    [
        ('title = "No number"\nbody = ""', "needs a number, a title and a body"),
        ('number = "101"\ntitle = "x"\nbody = ""', "needs a number"),
        ('number = 100\ntitle = "x"\nbody = ""', "page numbers go from 101 to 899"),
    ],
)
def test_articles_that_will_not_do(tmp_path, text, complaint):
    with pytest.raises(ContentError, match=complaint):
        load(write(tmp_path, "bad.toml", text))


def test_two_pages_cannot_share_a_number(tmp_path):
    write(tmp_path, "a.toml", GOOD)
    write(tmp_path, "b.toml", GOOD)
    with pytest.raises(ContentError, match="two pages numbered 101"):
        load_all(tmp_path)


def test_paragraphs_are_wrapped_and_coloured_lines_are_coloured():
    lines = lines_of("{yellow}HEADLINE\n\n" + "word " * 20)
    assert lines[0] == ("HEADLINE", Colour.YELLOW)
    assert lines[1] == ("", Colour.WHITE)
    assert all(len(text) <= 38 for text, _ink in lines)
    assert len(lines) == 5
    with pytest.raises(ContentError, match="no such colour as puce"):
        lines_of("{puce}Oh dear")


def test_neighbours():
    known = {100, 101, 102, 301}
    assert neighbours(100, known) == (None, 101)
    assert neighbours(102, known) == (101, 301)
    assert neighbours(301, known) == (102, None)


def test_the_site_has_an_index_and_numbers_become_links(tmp_path):
    write(tmp_path, "a.toml", GOOD)
    write(tmp_path, "b.toml", GOOD.replace("101", "102").replace("Hello", "Again"))
    index, first, second = pages(tmp_path, TODAY)
    listed = [line for line in index.text().splitlines() if "..." in line]
    assert listed == [" Hello" + "." * 30 + "101", " Again" + "." * 30 + "102"]
    assert all(len(line) == COLUMNS - 1 for line in listed)
    assert (first.before, first.after, second.after) == (100, 102, None)

    row = next(row for row in first.rows if "See 102" in "".join(c.text for c in row))
    links = [cell.link for cell in row if cell.link]
    assert links == [102, 102, 102]  # and 999 isn't a page, so it isn't a link


def test_a_page_that_is_too_long_is_refused(tmp_path):
    write(tmp_path, "a.toml", GOOD.replace("See 102", "word " * 200))
    with pytest.raises(ContentError, match=r"Page 101 is \d+ lines too long"):
        pages(tmp_path, TODAY)
