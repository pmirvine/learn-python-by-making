from pyfax import COLUMNS, ROWS, Cell, Colour, Page
from pyfax.font import banner


def test_colours_are_made_of_three_bits():
    assert Colour.RED | Colour.GREEN == Colour.YELLOW
    assert Colour.RED | Colour.GREEN | Colour.BLUE == Colour.WHITE
    assert Colour.WHITE ^ Colour.YELLOW == Colour.BLUE
    assert [colour.css for colour in (Colour.BLACK, Colour.YELLOW, Colour.CYAN)] == [
        "#000",
        "#ff0",
        "#0ff",
    ]


def test_a_new_page_is_blank_and_the_right_size():
    page = Page(100, "Index")
    assert len(page.rows) == ROWS
    assert all(len(row) == COLUMNS for row in page.rows)
    assert page.text().strip() == ""


def test_the_rows_of_a_page_are_not_all_one_list():
    page = Page(100, "Index")
    page.write(0, 0, "X")
    assert page.rows[1][0] == Cell()


def test_writing_clips_at_the_edges():
    page = Page(100, "Index")
    page.write(3, 36, "EIGHT", Colour.YELLOW, link=108)
    page.write(99, 0, "nowhere")
    assert page.text().splitlines()[3].endswith("EIGH")
    assert page.rows[3][39] == Cell("H", Colour.YELLOW, link=108)


def test_a_picture_becomes_graphics_characters():
    page = Page(100, "Index")
    page.picture(2, 5, ["####", "####", "####"], Colour.RED)
    assert page.rows[2][5] == Cell(ink=Colour.RED, dots=63)
    assert page.rows[2][6].dots == 63
    assert page.rows[2][7] == Cell()


def test_a_banner_is_six_pixels_high_and_four_wide_for_each_letter():
    rows = banner("Hi!")
    assert len(rows) == 6
    assert {len(row) for row in rows} == {12}
    assert rows[0] == "#.#.###..#.."
    assert banner("~")[0] == "###."
