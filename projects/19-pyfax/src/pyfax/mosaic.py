"""Teletext's block graphics: six little squares to a character, and a bit for each."""

from enum import IntFlag


class Dot(IntFlag):
    """The six squares of a graphics character, two across and three down."""

    TOP_LEFT = 1
    TOP_RIGHT = 2
    MIDDLE_LEFT = 4
    MIDDLE_RIGHT = 8
    BOTTOM_LEFT = 16
    BOTTOM_RIGHT = 32


ALL_DOTS = 0b111111


def pack(bitmap: list[str]) -> list[list[int]]:
    """Turn a picture into rows of graphics characters.

    The picture is some strings, in which anything but a full stop or a space is
    a lit pixel. Each character takes in a patch two pixels wide and three high.
    """
    height = len(bitmap)
    width = max((len(row) for row in bitmap), default=0)

    def lit(x: int, y: int) -> bool:
        return y < height and x < len(bitmap[y]) and bitmap[y][x] not in ". "

    rows: list[list[int]] = []
    for top in range(0, height, 3):
        row: list[int] = []
        for left in range(0, width, 2):
            dots = 0
            for position in range(6):
                if lit(left + position % 2, top + position // 2):
                    dots |= 1 << position
            row.append(dots)
        rows.append(row)
    return rows


def unpack(dots: int) -> list[str]:
    """Turn one graphics character back into three rows of two pixels."""
    return [
        "".join("#" if dots & (1 << (y * 2 + x)) else "." for x in range(2))
        for y in range(3)
    ]


def stylesheet() -> str:
    """Return the CSS for the 63 graphics characters that have anything in them.

    It's worked out from their bits. Each lit square is a block of the cell's own
    text colour, painted as a background image, in the right sixth of the cell.
    """
    rules: list[str] = []
    for dots in range(1, ALL_DOTS + 1):
        lit = [position for position in range(6) if dots >> position & 1]
        images = ", ".join("linear-gradient(currentColor, currentColor)" for _ in lit)
        places = ", ".join(f"{p % 2 * 100}% {p // 2 * 50}%" for p in lit)
        rules.append(
            f".m{dots} {{ background-image: {images}; background-position: {places}; }}"
        )
    return "\n".join(rules) + "\n"
