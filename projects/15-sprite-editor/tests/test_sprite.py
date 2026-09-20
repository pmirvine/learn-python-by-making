import pytest

from sprite_editor.sprite import Sprite, SpriteError

INVADER = """\
sprite 8 6
..2..2..
...22...
..2222..
.22.22.2
22222222
2.2..2.2
"""


def test_pixels_are_see_through_until_they_are_set():
    sprite = Sprite(4, 4)
    assert sprite[1, 2] is None
    sprite[1, 2] = 5
    assert sprite[1, 2] == 5
    sprite[1, 2] = None
    assert sprite.pixels == {}


def test_what_is_in_a_sprite():
    sprite = Sprite(4, 3)
    assert (3, 2) in sprite
    assert (4, 2) not in sprite
    assert (0, -1) not in sprite
    with pytest.raises(IndexError, match="isn't in a 4 by 3 sprite"):
        sprite[4, 2] = 1


def test_text_goes_there_and_back():
    invader = Sprite.from_text(INVADER)
    assert (invader.width, invader.height) == (8, 6)
    assert invader[2, 0] == 2
    assert invader[0, 0] is None
    assert invader.to_text() == INVADER


def test_comments_and_blank_lines_are_ignored():
    text = "# An invader\n\n" + INVADER.replace("\n", "\n\n")
    assert Sprite.from_text(text) == Sprite.from_text(INVADER)


def test_files_go_there_and_back(tmp_path):
    path = tmp_path / "invader.sprite"
    Sprite.from_text(INVADER).save(path)
    assert path.read_text(encoding="utf-8") == INVADER
    assert Sprite.load(path) == Sprite.from_text(INVADER)


@pytest.mark.parametrize(
    ("old", "new", "complaint"),
    [
        ("sprite 8 6", "sprite 8", "the first line should be like"),
        ("sprite 8 6", "sprite eight 6", "the first line should be like"),
        ("sprite 8 6", "sprite 8 7", "there are 6 rows, and not 7"),
        ("...22...", "...22..", "row 1 is 7 long, and not 8"),
        ("...22...", "...2A...", "row 1 has a 'A' in it"),
        (INVADER, "", "the first line should be like"),
    ],
)
def test_bad_files_are_reported(old, new, complaint):
    assert old in INVADER
    with pytest.raises(SpriteError, match=complaint):
        Sprite.from_text(INVADER.replace(old, new))


def test_a_subclass_makes_its_own_kind():
    class Stamp(Sprite):
        pass

    assert type(Stamp.from_text(INVADER)) is Stamp
