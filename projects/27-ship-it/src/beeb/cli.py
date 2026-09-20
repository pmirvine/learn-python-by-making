"""The `beeb` command: a test card. Eight bars and a beep mean that everything works."""

import argparse

from beeb import HEIGHT, WIDTH, __version__, draw, gcol, mode, move, plot, sound, vsync


def block(left: int, bottom: int, right: int, top: int) -> None:
    """Fill a rectangle the way BBC programs did: as two triangles."""
    move(left, bottom)
    move(right, bottom)
    plot(85, left, top)
    plot(85, right, top)


def test_card() -> None:
    mode(2)
    bar = WIDTH // 8
    for colour in range(8):
        gcol(0, colour)
        block(colour * bar, 128, (colour + 1) * bar - 1, HEIGHT - 1)

    gcol(0, 7)
    for x in range(0, WIDTH, 64):
        move(x, 0)
        draw(x, 96)


def main() -> None:
    parser = argparse.ArgumentParser(prog="beeb", description=__doc__)
    parser.add_argument("--version", action="version", version=f"beeb {__version__}")
    parser.parse_args()

    test_card()
    sound(1, -12, 101, 6)
    while True:
        vsync()
