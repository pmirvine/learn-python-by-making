"""Extend 2: TOUCH(n). Is a sprite over anything that's been drawn on the screen?

It's the landscape, in a game of landing, and the walls, in a maze. Call
install_touch(micro) after the computer has been made.
"""

import beeb
import pygame
from tiny_basic.registry import function
from tiny_basic.values import FALSE, TRUE, number

from micro.basic import complaining
from micro.computer import Micro
from micro.sprites import SpriteLayer


def touching(
    layer: SpriteLayer, n: int, canvas: pygame.Surface, paper: int = 0
) -> bool:
    """Make a mask of everything that isn't background, and lay the sprite's mask over it."""
    picture = canvas.copy()
    picture.set_colorkey(picture.get_palette_at(paper))
    drawn = pygame.mask.from_surface(picture)
    return drawn.overlap(layer.slot(n).mask, layer.box(n).topleft) is not None


def install_touch(micro: Micro) -> None:
    @function("TOUCH")
    def touch(n: float) -> float:  # pyright: ignore[reportUnusedFunction]
        with complaining():
            found = touching(micro.sprites, int(number(n)), beeb.canvas())
        return TRUE if found else FALSE
