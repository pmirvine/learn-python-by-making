"""A teletext page: twenty-five rows of forty cells."""

from dataclasses import dataclass, field
from enum import IntEnum

from pyfax.mosaic import pack

COLUMNS = 40
ROWS = 25


class Colour(IntEnum):
    """Teletext's eight colours. There's a bit each for red, green and blue."""

    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7

    @property
    def css(self) -> str:
        """The colour as a web page writes it: #ff0 is red and green, and no blue."""
        red, green, blue = ("f" if self & bit else "0" for bit in (1, 2, 4))
        return f"#{red}{green}{blue}"


@dataclass(frozen=True, slots=True)
class Cell:
    text: str = " "
    ink: Colour = Colour.WHITE
    paper: Colour = Colour.BLACK
    dots: int | None = None  # for a graphics character: which squares are lit
    link: int | None = None  # the number of the page that this cell leads to


BLANK = Cell()


def blank_rows() -> list[list[Cell]]:
    return [[BLANK] * COLUMNS for _ in range(ROWS)]


@dataclass
class Page:
    number: int
    title: str
    section: str = ""
    before: int | None = None  # the pages on either side of this one, if there are any
    after: int | None = None
    rows: list[list[Cell]] = field(default_factory=blank_rows)

    def write(
        self,
        row: int,
        column: int,
        text: str,
        ink: Colour = Colour.WHITE,
        paper: Colour = Colour.BLACK,
        link: int | None = None,
    ) -> None:
        """Put some text on the page. Whatever runs off the right-hand edge is lost."""
        for offset, character in enumerate(text):
            if 0 <= row < ROWS and 0 <= column + offset < COLUMNS:
                self.rows[row][column + offset] = Cell(character, ink, paper, link=link)

    def picture(self, row: int, column: int, bitmap: list[str], ink: Colour) -> None:
        """Put a picture on the page, in graphics characters."""
        for down, line in enumerate(pack(bitmap)):
            for across, dots in enumerate(line):
                if 0 <= row + down < ROWS and 0 <= column + across < COLUMNS:
                    self.rows[row + down][column + across] = Cell(ink=ink, dots=dots)

    def fill(self, row: int, paper: Colour) -> None:
        """Give a whole row a background colour."""
        self.rows[row] = [Cell(paper=paper)] * COLUMNS

    def text(self) -> str:
        """Return the page as plain text, with a # for every graphics character."""
        return "\n".join(
            "".join("#" if cell.dots else cell.text for cell in row).rstrip()
            for row in self.rows
        )
