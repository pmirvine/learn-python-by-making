from pathlib import Path

import pytest

from micro.sprites import Edge, SpriteLayer

MODE_1 = (320, 256)  # four screen units to a pixel, each way
CORNER = "sprite 4 4\n11..\n11..\n....\n....\n"
SQUARE = "sprite 4 4\n2222\n2222\n2222\n2222\n"


@pytest.fixture
def layer(tmp_path: Path) -> SpriteLayer:
    (tmp_path / "corner.sprite").write_text(CORNER, encoding="utf-8")
    (tmp_path / "square.sprite").write_text(SQUARE, encoding="utf-8")
    layer = SpriteLayer(MODE_1)
    layer.define(1, tmp_path / "corner.sprite")
    layer.define(2, tmp_path / "square.sprite")
    return layer


def test_a_sprite_is_put_by_its_bottom_left_hand_corner(layer: SpriteLayer):
    layer.put(2, 0, 0)
    assert layer.box(2).bottomleft == (0, 256)
    layer.put(2, 400, 512)
    assert layer.box(2).topleft == (100, 124)


def test_sprites_that_are_apart_are_not_touching(layer: SpriteLayer):
    layer.put(1, 0, 0)
    layer.put(2, 400, 400)
    assert not layer.collide(1, 2)


def test_boxes_may_overlap_where_pixels_do_not(layer: SpriteLayer):
    layer.put(1, 100, 100)
    layer.put(
        2, 108, 108
    )  # two pixels right, and two up: over the corner's empty part...
    assert layer.box(1).colliderect(layer.box(2))
    assert not layer.collide(1, 2)
    layer.put(2, 104, 108)  # ...and one pixel back: now the solid parts meet
    assert layer.collide(1, 2)
    assert layer.collide(2, 1)


def test_a_hidden_sprite_touches_nothing(layer: SpriteLayer):
    layer.put(1, 100, 100)
    layer.put(2, 100, 100)
    assert layer.collide(1, 2)
    layer.hide(2)
    assert not layer.collide(1, 2)


def test_edges(layer: SpriteLayer):
    layer.put(2, 640, 512)
    assert layer.edge(2) == Edge(0)
    layer.put(2, -4, 512)
    assert layer.edge(2) == Edge.LEFT
    layer.put(2, 1268, 1012)
    assert layer.edge(2) == Edge.RIGHT | Edge.TOP
    layer.put(2, 640, -4)
    assert layer.edge(2) == Edge.BOTTOM


def test_a_sprite_that_is_just_inside_is_not_over_the_edge(layer: SpriteLayer):
    layer.put(2, 1264, 1008)  # four pixels from the right, and four from the top
    assert layer.edge(2) == Edge(0)


def test_complaints(layer: SpriteLayer, tmp_path: Path):
    with pytest.raises(ValueError, match="No such sprite"):
        layer.put(9, 0, 0)
    with pytest.raises(ValueError, match="Bad sprite"):
        layer.define(16, tmp_path / "square.sprite")
    with pytest.raises(ValueError, match="Sprite not found: nothing"):
        layer.define(3, tmp_path / "nothing.sprite")
    (tmp_path / "broken.sprite").write_text("sprite 2 2\n11\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Bad sprite broken: there are 1 rows"):
        layer.define(3, tmp_path / "broken.sprite")
