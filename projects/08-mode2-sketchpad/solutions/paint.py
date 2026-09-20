"""The paint program with the challenges added.

Drag with the left button to draw, or the right button to rub out.
Keys: 0-7 choose a colour, F fills from the mouse pointer, M turns four-way
mirroring on and off, C clears, S saves masterpiece.png. Escape quits.

Run it from the project folder with `uv run solutions/paint.py`. Python looks
for imports next to the script first, so it picks up the extended beeb package
in this folder rather than the one in src/.
"""

import beeb

SWATCH = 64

type Point = tuple[int, int]


def square(size: int, colour: int) -> None:
    """Fill a square in the bottom-left corner, as two triangles."""
    beeb.gcol(0, colour)
    beeb.move(0, 0)
    beeb.move(size, 0)
    beeb.plot(85, 0, size)
    beeb.plot(85, size, size)


def show_colour(colour: int, mirrored: bool) -> None:
    """Show the current colour as a swatch. Its border goes red when mirroring."""
    square(SWATCH + 16, 1 if mirrored else 7)
    square(SWATCH, colour)


def reflections(point: Point, mirrored: bool) -> list[Point]:
    """Return the point, plus its three mirror images if mirroring is on."""
    x, y = point
    if not mirrored:
        return [point]
    across, up = beeb.WIDTH - 1 - x, beeb.HEIGHT - 1 - y
    return [(x, y), (across, y), (x, up), (across, up)]


def main() -> None:
    beeb.mode(2)
    colour = 7
    mirrored = False
    last: Point | None = None

    while True:
        x, y, (left, _, right) = beeb.mouse()

        key = beeb.inkey().lower()
        if key.isdigit() and int(key) < 8:
            colour = int(key)
        elif key == "c":
            beeb.clg()
        elif key == "s":
            beeb.screenshot("masterpiece.png")
        elif key == "m":
            mirrored = not mirrored
        elif key == "f":
            beeb.gcol(0, colour)
            for fx, fy in reflections((x, y), mirrored):
                beeb.fill(fx, fy)

        if left or right:
            beeb.gcol(0, colour if left else 0)
            starts = reflections(last or (x, y), mirrored)
            ends = reflections((x, y), mirrored)
            for start, end in zip(starts, ends, strict=True):
                beeb.move(*start)
                beeb.draw(*end)
            last = (x, y)
        else:
            last = None

        show_colour(colour, mirrored)
        beeb.vsync()


if __name__ == "__main__":
    main()
