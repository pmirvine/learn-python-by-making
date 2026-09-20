"""Stage 3: the three layers, with nothing behind them yet. Escape, or close the window."""

import beeb
import pygame
from pyfax import Colour
from pyfax.font import banner

from micro.display import Display
from micro.sprites import SpriteLayer
from micro.textscreen import TextScreen


def main(frames: int | None = None) -> None:
    beeb.mode(1)
    beeb.gcol(0, 1)
    for x in range(0, 1280, 32):
        beeb.move(x, 0)
        beeb.draw(1279 - x, 1023)

    screen = TextScreen()
    screen.page.picture(1, 2, banner("MICRO"), Colour.YELLOW)
    screen.move_to(0, 5)
    screen.write("Text, over graphics, in the same window.\n\n>")

    display, clock, count = Display(), pygame.time.Clock(), 0
    while frames is None or count < frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                return
        count += 1
        display.show(
            beeb.canvas(),
            SpriteLayer(beeb.canvas().get_size()),
            screen,
            count % 32 < 16,
        )
        clock.tick(50)


if __name__ == "__main__":
    main()
