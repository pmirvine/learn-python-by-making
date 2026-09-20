from pyfax import COLUMNS, ROWS, Colour

from micro.editor import LONGEST, LineEditor
from micro.textscreen import RUB_OUT, TextScreen


def test_writing_moves_the_cursor():
    screen = TextScreen()
    screen.write("HELLO")
    assert screen.text() == "HELLO"
    assert (screen.column, screen.row) == (5, 0)


def test_a_new_line():
    screen = TextScreen()
    screen.write("ONE\nTWO")
    assert screen.text().splitlines() == ["ONE", "TWO"]


def test_a_long_line_wraps_at_forty_columns():
    screen = TextScreen()
    screen.write("*" * (COLUMNS + 2))
    assert screen.text().splitlines() == ["*" * COLUMNS, "**"]


def test_at_the_bottom_everything_moves_up():
    screen = TextScreen()
    for number in range(ROWS + 2):
        screen.write(f"LINE {number}\n")
    shown = screen.text().splitlines()
    assert shown[0] == "LINE 3"
    assert shown[-1] == f"LINE {ROWS + 1}"
    assert screen.row == ROWS - 1
    assert len(screen.page.rows) == ROWS


def test_rubbing_out():
    screen = TextScreen()
    screen.write("CAT" + RUB_OUT + "N")
    assert screen.text() == "CAN"


def test_rubbing_out_goes_back_up_a_line():
    screen = TextScreen()
    screen.write("*" * COLUMNS + "!" + RUB_OUT + RUB_OUT)
    assert screen.text() == "*" * (COLUMNS - 1)
    assert (screen.column, screen.row) == (COLUMNS - 1, 0)


def test_the_cursor_cannot_be_put_off_the_screen():
    screen = TextScreen()
    screen.move_to(99, -5)
    assert (screen.column, screen.row) == (COLUMNS - 1, 0)


def test_text_is_written_in_the_current_colour():
    screen = TextScreen()
    screen.ink = Colour.YELLOW
    screen.write("!")
    assert screen.page.rows[0][0].ink == Colour.YELLOW


def test_the_editor_echoes_what_is_typed_and_hands_the_line_over():
    screen = TextScreen()
    editor = LineEditor(screen)
    for character in "PRIMT":
        editor.type(character)
    editor.rub_out()
    editor.rub_out()
    editor.type("N")
    editor.type("T")
    assert screen.text() == "PRINT"
    assert editor.take() == "PRINT"
    assert editor.line == ""
    assert screen.row == 1


def test_the_editor_ignores_what_cannot_be_printed_and_lines_that_are_too_long():
    editor = LineEditor(TextScreen())
    editor.type("\t")
    editor.rub_out()
    for _ in range(LONGEST + 10):
        editor.type("A")
    assert len(editor.line) == LONGEST
