"""One character for each of teletext's 64 graphics characters."""

FIRST_SEXTANT = 0x1FB00
LEFT_HALF, RIGHT_HALF, FULL = 0b010101, 0b101010, 0b111111

# Braille has two columns of four dots. These are the bits for the dots that
# stand in for each of our six squares: the middle pair of rows both do for the middle.
BRAILLE = 0x2800
BRAILLE_DOTS = [0x01, 0x08, 0x02 | 0x04, 0x10 | 0x20, 0x40, 0x80]


def sextant(dots: int) -> str:
    """Return the Unicode "sextant" for a pattern of six squares.

    Unicode 13 added these for the sake of teletext. There are 60 of them, since
    four of the 64 patterns were in Unicode already: nothing, everything, and
    the left and right halves.
    """
    ready_made = {0: " ", LEFT_HALF: "▌", RIGHT_HALF: "▐", FULL: "█"}
    if dots in ready_made:
        return ready_made[dots]
    skipped = (dots > LEFT_HALF) + (dots > RIGHT_HALF)
    return chr(FIRST_SEXTANT + dots - 1 - skipped)


def braille(dots: int) -> str:
    """Return a Braille pattern that looks something like it, for older fonts."""
    pattern = sum(BRAILLE_DOTS[n] for n in range(6) if dots >> n & 1)
    return chr(BRAILLE + pattern)


QUADRANTS = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"


def quadrant(dots: int) -> str:
    """Return a character of four squares, which every font has, as near as can be had.

    The top row of squares stays as it is. The middle and the bottom rows have to
    share the lower half of the character, and so a square there is lit if either is.
    """
    top = dots & 0b11
    lower = (dots >> 2 | dots >> 4) & 0b11
    return QUADRANTS[top | lower << 2]


# The ways of drawing a graphics character, by name, for the command line.
GLYPHS = {"sextant": sextant, "quadrant": quadrant, "braille": braille}
