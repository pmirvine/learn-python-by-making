"""Hardware sprites, which the BBC Micro never had: pictures that float over the screen.

A sprite isn't drawn on the graphics screen. It's laid over it, afresh, in every
frame, and so moving one disturbs nothing underneath.
"""

from dataclasses import dataclass
from enum import IntFlag
from pathlib import Path

import pygame
from beeb.screen import COLOURS, to_pixel
from sprite_editor.sprite import Sprite, SpriteError

SLOTS = 16


class Edge(IntFlag):
    """Which sides of the screen a sprite has crossed. EDGE(n) adds these up."""

    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8


@dataclass
class Slot:
    image: pygame.Surface
    mask: pygame.Mask
    x: float = 0  # in screen units: the sprite's bottom left-hand corner
    y: float = 0
    showing: bool = False


def picture_of(sprite: Sprite) -> pygame.Surface:
    """Turn one of Project 15's sprites into a surface, see-through where it's clear."""
    image = pygame.Surface((sprite.width, sprite.height), pygame.SRCALPHA)
    for (x, y), colour in sprite.pixels.items():
        image.set_at((x, y), COLOURS[colour])
    return image


class SpriteLayer:
    def __init__(self, size: tuple[int, int]) -> None:
        self.size = (
            size  # of the graphics screen, in its own pixels, which vary with the mode
        )
        self.slots: dict[int, Slot] = {}

    def define(self, number: int, path: Path) -> None:
        if not 0 <= number < SLOTS:
            raise ValueError("Bad sprite")
        try:
            image = picture_of(Sprite.load(path))
        except OSError:
            raise ValueError(f"Sprite not found: {path.stem}") from None
        except SpriteError as error:
            raise ValueError(f"Bad sprite {path.stem}: {error}") from None
        self.slots[number] = Slot(image, pygame.mask.from_surface(image))

    def slot(self, number: int) -> Slot:
        if number not in self.slots:
            raise ValueError("No such sprite")
        return self.slots[number]

    def put(self, number: int, x: float, y: float) -> None:
        slot = self.slot(number)
        slot.x, slot.y, slot.showing = x, y, True

    def hide(self, number: int) -> None:
        self.slot(number).showing = False

    def box(self, number: int) -> pygame.Rect:
        """Return where a sprite is, in the pixels of the graphics screen."""
        slot = self.slot(number)
        left, bottom = to_pixel(slot.x, slot.y, *self.size)
        box = slot.image.get_rect()
        box.bottomleft = (left, bottom + 1)
        return box

    def collide(self, first: int, second: int) -> bool:
        """Are two sprites touching? Boxes first, which is quick. Then pixels."""
        a, b = self.slot(first), self.slot(second)
        if not (a.showing and b.showing):
            return False
        box_a, box_b = self.box(first), self.box(second)
        if not box_a.colliderect(box_b):
            return False
        offset = (box_b.x - box_a.x, box_b.y - box_a.y)
        return a.mask.overlap(b.mask, offset) is not None

    def edge(self, number: int) -> Edge:
        box = self.box(number)
        width, height = self.size
        found = Edge(0)
        if box.left < 0:
            found |= Edge.LEFT
        if box.right > width:
            found |= Edge.RIGHT
        if box.bottom > height:
            found |= Edge.BOTTOM
        if box.top < 0:
            found |= Edge.TOP
        return found

    def draw(self, picture: pygame.Surface) -> None:
        """Lay every sprite that's showing over a picture, lowest number on top."""
        for number in sorted(self.slots, reverse=True):
            if self.slots[number].showing:
                picture.blit(self.slots[number].image, self.box(number))
