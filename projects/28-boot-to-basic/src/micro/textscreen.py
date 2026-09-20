"""The text screen: forty columns, twenty-five rows, a cursor, and a scroll.

The page underneath is Project 19's. There's no Pygame in here.
"""

from pyfax import COLUMNS, ROWS, Cell, Colour, Page
from pyfax.page import BLANK

RUB_OUT = "\x7f"


class TextScreen:
    def __init__(self) -> None:
        self.page = Page(0, "The screen")
        self.column = 0
        self.row = 0
        self.ink = Colour.WHITE

    def clear(self) -> None:
        self.page.rows[:] = [[BLANK] * COLUMNS for _ in range(ROWS)]
        self.column = self.row = 0

    def move_to(self, column: int, row: int) -> None:
        """Put the cursor somewhere, as TAB(x, y) does."""
        self.column = max(0, min(COLUMNS - 1, column))
        self.row = max(0, min(ROWS - 1, row))

    def write(self, text: str) -> None:
        for character in text:
            if character == "\n":
                self.new_line()
            elif character == RUB_OUT:
                self.rub_out()
            else:
                self.page.rows[self.row][self.column] = Cell(character, self.ink)
                self.column += 1
                if self.column == COLUMNS:
                    self.new_line()

    def new_line(self) -> None:
        self.column = 0
        if self.row < ROWS - 1:
            self.row += 1
        else:  # at the bottom, everything moves up, and the top line is lost
            del self.page.rows[0]
            self.page.rows.append([BLANK] * COLUMNS)

    def rub_out(self) -> None:
        """Step back one place, and blank it. At the left, go up to the line before."""
        if self.column > 0:
            self.column -= 1
        elif self.row > 0:
            self.row -= 1
            self.column = COLUMNS - 1
        self.page.rows[self.row][self.column] = BLANK

    def text(self) -> str:
        """Return what's on the screen, without the empty lines at the bottom."""
        return self.page.text().rstrip("\n")
