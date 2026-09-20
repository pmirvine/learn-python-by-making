"""BBC Micro-style graphics commands, built on Pygame."""

from beeb.screen import (
    HEIGHT,
    WIDTH,
    clg,
    draw,
    gcol,
    inkey,
    mode,
    mouse,
    move,
    plot,
    point,
    screenshot,
    vsync,
)

__all__ = [
    "HEIGHT",
    "WIDTH",
    "clg",
    "draw",
    "gcol",
    "inkey",
    "mode",
    "mouse",
    "move",
    "plot",
    "point",
    "screenshot",
    "vsync",
]


def block(left: int, bottom: int, right: int, top: int) -> None:
    """Fill a rectangle the way BBC programs did: as two triangles."""
    move(left, bottom)
    move(right, bottom)
    plot(85, left, top)
    plot(85, right, top)


def main() -> None:
    """Show a test card: if you can see eight colour bars, everything works."""
    mode(2)
    bar = WIDTH // 8
    for colour in range(8):
        gcol(0, colour)
        block(colour * bar, 128, (colour + 1) * bar - 1, HEIGHT - 1)

    gcol(0, 7)
    for x in range(0, WIDTH, 64):
        move(x, 0)
        draw(x, 96)

    while True:
        vsync()
