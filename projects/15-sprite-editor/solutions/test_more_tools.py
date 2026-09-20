import pytest
from more_tools import Ellipse, FilledBox, Turn

from sprite_editor.sprite import Sprite
from sprite_editor.tools import ShapeTool


def drawn(tool: ShapeTool, start, end, size=9) -> str:
    sprite = Sprite(size, size)
    tool.press(sprite, start, 1)
    tool.drag(sprite, end)
    command = tool.release(sprite)
    assert command is not None
    command.do(sprite)
    return "\n".join(sprite.to_text().splitlines()[1:])


def test_a_block_is_full():
    assert drawn(FilledBox(), (3, 1), (1, 2), size=5) == (
        ".....\n.111.\n.111.\n.....\n....."
    )


def test_an_oval_is_hollow_and_symmetrical():
    picture = drawn(Ellipse(), (0, 1), (8, 7))
    rows = picture.splitlines()
    assert rows == rows[::-1]
    assert all(row == row[::-1] for row in rows)
    assert rows[4] == "1.......1"
    assert rows[0] == "........."
    assert "1" in rows[1]


def test_a_turn_and_back():
    sprite = Sprite.from_text("sprite 3 3\n12.\n...\n...\n")
    turn = Turn()
    turn.do(sprite)
    assert sprite.to_text() == "sprite 3 3\n..1\n..2\n...\n"
    turn.undo(sprite)
    assert sprite.to_text() == "sprite 3 3\n12.\n...\n...\n"


def test_an_oblong_cannot_be_turned():
    with pytest.raises(ValueError, match="square"):
        Turn().do(Sprite(4, 3))
