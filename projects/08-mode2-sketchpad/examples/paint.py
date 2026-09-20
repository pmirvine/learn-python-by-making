"""A tiny paint program.

Drag with the left button to draw. Keys: 0-7 choose a colour, C clears the
screen, S saves masterpiece.png. Escape quits.
"""

import beeb

SWATCH = 64


def square(size: int, colour: int) -> None:
    """Fill a square in the bottom-left corner, as two triangles."""
    beeb.gcol(0, colour)
    beeb.move(0, 0)
    beeb.move(size, 0)
    beeb.plot(85, 0, size)
    beeb.plot(85, size, size)


def show_colour(colour: int) -> None:
    """Show the current colour as a swatch with a white border."""
    square(SWATCH + 16, 7)
    square(SWATCH, colour)


def main() -> None:
    beeb.mode(2)
    colour = 7
    last: tuple[int, int] | None = None

    while True:
        key = beeb.inkey().lower()
        if key.isdigit() and int(key) < 8:
            colour = int(key)
        elif key == "c":
            beeb.clg()
        elif key == "s":
            beeb.screenshot("masterpiece.png")

        x, y, (left, _, _) = beeb.mouse()
        if left:
            beeb.gcol(0, colour)
            beeb.move(*(last or (x, y)))
            beeb.draw(x, y)
            last = (x, y)
        else:
            last = None

        show_colour(colour)
        beeb.vsync()


if __name__ == "__main__":
    main()
