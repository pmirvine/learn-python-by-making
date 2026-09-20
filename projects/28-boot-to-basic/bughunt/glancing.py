"""A colleague's version of the collision test. "It mostly works."

    uv run bughunt/glancing.py

In their game, some bolts go clean through the alien, and others hit thin air.
"""

import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from sprite_editor.sprite import Sprite

from micro.sprites import Slot, SpriteLayer, picture_of

# Each is four pixels square, and only a quarter of it is solid.
LOW_LEFT = "sprite 4 4\n....\n....\n11..\n11..\n"
HIGH_RIGHT = "sprite 4 4\n..22\n..22\n....\n....\n"


class Layer(SpriteLayer):
    def collide(self, first: int, second: int) -> bool:
        a, b = self.slot(first), self.slot(second)
        if not (a.showing and b.showing):
            return False
        box_a, box_b = self.box(first), self.box(second)
        if not box_a.colliderect(box_b):
            return False
        offset = (box_a.x - box_b.x, box_a.y - box_b.y)
        return a.mask.overlap(b.mask, offset) is not None


def two_sprites() -> Layer:
    layer = Layer((320, 256))  # MODE 1, in which a pixel is four units each way
    for number, text in [(1, LOW_LEFT), (2, HIGH_RIGHT)]:
        image = picture_of(Sprite.from_text(text))
        layer.slots[number] = Slot(image, pygame.mask.from_surface(image))
    return layer


if __name__ == "__main__":
    layer = two_sprites()
    layer.put(1, 400, 400)
    layer.put(2, 392, 392)  # two pixels left, and two down: the solid parts coincide
    print("One right on top of the other. Touching?", layer.collide(1, 2))
    layer.put(2, 408, 408)  # two pixels right, and two up: they're six pixels apart
    print("Nowhere near each other.       Touching?", layer.collide(1, 2))
