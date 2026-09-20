"""The bug hunt's failing tests. They pass with the real SpriteLayer.

The mended line, in collide():

    offset = (box_b.x - box_a.x, box_b.y - box_a.y)

overlap() wants to know where the *other* mask is, as seen from this one.
"""

import sys
from pathlib import Path

import pygame
import pytest
from sprite_editor.sprite import Sprite

from micro.sprites import Slot, SpriteLayer, picture_of

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "bughunt"))
from glancing import HIGH_RIGHT, LOW_LEFT, Layer


def two_sprites(kind: type[SpriteLayer]) -> SpriteLayer:
    layer = kind((320, 256))
    for number, text in [(1, LOW_LEFT), (2, HIGH_RIGHT)]:
        image = picture_of(Sprite.from_text(text))
        layer.slots[number] = Slot(image, pygame.mask.from_surface(image))
    layer.put(1, 400, 400)
    return layer


@pytest.mark.parametrize(("x", "y", "touching"), [(392, 392, True), (408, 408, False)])
def test_the_real_layer_knows_which_way_is_which(x: int, y: int, touching: bool):
    layer = two_sprites(SpriteLayer)
    layer.put(2, x, y)
    assert layer.collide(1, 2) is touching
    assert layer.collide(2, 1) is touching


def test_the_colleagues_layer_has_it_backwards():
    layer = two_sprites(Layer)
    layer.put(2, 392, 392)
    assert not layer.collide(1, 2)  # a bolt goes clean through
    layer.put(2, 408, 408)
    assert layer.collide(1, 2)  # and another hits thin air
