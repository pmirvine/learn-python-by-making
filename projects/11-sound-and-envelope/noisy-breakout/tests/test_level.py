import pytest

from breakout.model import Level

PICTURE = """
    R.G
    .#.
"""


def test_a_level_is_built_from_a_picture():
    level = Level.from_text(PICTURE, name="tiny")
    assert len(level.bricks) == 3
    red, green, tough = level.bricks
    assert (red.colour, red.points, red.hits) == ("red", 50, 1)
    assert (green.rect.left, green.rect.top) == (40, 24)
    assert (tough.rect.left, tough.rect.top, tough.hits) == (20, 32, 2)


def test_a_level_describes_itself():
    assert repr(Level.from_text(PICTURE, name="tiny")) == "Level('tiny', 3 bricks)"


def test_unknown_bricks_are_reported_with_their_row():
    with pytest.raises(ValueError, match=r"Unknown brick '\?' in row 2"):
        Level.from_text("RRR\nR?R")


def test_a_level_can_come_from_a_file(tmp_path):
    file = tmp_path / "9-test.txt"
    file.write_text("YY\n", encoding="utf-8")
    level = Level.from_file(file)
    assert level.name == "9-test"
    assert len(level.bricks) == 2


def test_the_built_in_levels_load_in_order():
    levels = Level.built_in()
    assert [level.name for level in levels] == ["1-wall", "2-invader", "3-fortress"]
    assert all(level.bricks for level in levels)


def test_hitting_a_brick_removes_it():
    level = Level.from_text("R")
    brick = level.bricks[0]
    assert level.hit_by(brick.rect.move(5, 5)) is brick
    assert level.cleared


def test_a_tough_brick_takes_two_hits():
    level = Level.from_text("#")
    target = level.bricks[0].rect
    assert level.hit_by(target) is not None
    assert not level.cleared
    assert level.hit_by(target) is not None
    assert level.cleared


def test_a_miss_is_none():
    level = Level.from_text("R")
    assert level.hit_by(level.bricks[0].rect.move(100, 100)) is None
    assert not level.cleared
