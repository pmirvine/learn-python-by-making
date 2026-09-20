"""Drawing the map, in box-drawing characters. There's no Textual in here."""

from adventure.game import Chart, Place

WIDE = 10  # the width of a room, including its walls
PITCH = WIDE + 1  # from one room's left wall to the next one's
MIDDLE = WIDE // 2

# Corners, walls and doorways: single lines for a room, double for the one you're in.
SINGLE = "┌─┐│└┘┴┬├┤"
DOUBLE = "╔═╗║╚╝╧╤╟╢"


def draw(chart: Chart) -> list[str]:
    """Return the floor that the player is on, as lines of text."""
    rooms = [place for place in chart.places if place.floor == chart.here.floor]
    left = min(place.x for place in rooms)
    top = min(place.y for place in rooms)
    columns = (max(place.x for place in rooms) - left + 1) * PITCH + 1
    rows = (max(place.y for place in rooms) - top + 1) * 3
    grid = [[" "] * columns for _ in range(rows)]

    for place in rooms:
        lines = SINGLE if place != chart.here else DOUBLE
        room(grid, place, 1 + (place.x - left) * PITCH, (place.y - top) * 3, lines)
    return ["".join(row).rstrip() for row in grid]


def room(grid: list[list[str]], place: Place, x: int, y: int, lines: str) -> None:
    """Draw one room, with its top left-hand corner at column x of row y."""
    top_left, flat, top_right, upright, bottom_left, bottom_right, n, s, e, w = lines
    label = f"{place.label[: WIDE - 2]:^{WIDE - 2}}"
    top = top_left + flat * (WIDE - 2) + top_right
    bottom = bottom_left + flat * (WIDE - 2) + bottom_right
    for row, text in enumerate([top, upright + label + upright, bottom]):
        grid[y + row][x : x + WIDE] = text

    marks = {
        "n": (y, x + MIDDLE, n),
        "s": (y + 2, x + MIDDLE, s),
        "w": (y + 1, x, w),
        "e": (y + 1, x + WIDE - 1, e),
        "u": (y, x + WIDE - 3, "▲"),
        "d": (y + 2, x + WIDE - 3, "▼"),
    }
    for exit in place.exits:
        row, column, mark = marks[exit]
        grid[row][column] = mark
    # A passage to the east or west shows in the gap between two rooms.
    if "w" in place.exits:
        grid[y + 1][x - 1] = "─"
    if "e" in place.exits:
        grid[y + 1][x + WIDE] = "─"
