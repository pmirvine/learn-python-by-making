import pytest

from sprite_editor.commands import Paint
from sprite_editor.shapes import box, cells_between, flood
from sprite_editor.sprite import Sprite
from sprite_editor.tools import (
    Box,
    Bucket,
    Eraser,
    Line,
    Pencil,
    Picker,
    ShapeTool,
    Tool,
)

RING = """\
sprite 5 5
.....
.111.
.1.1.
.111.
.....
"""


@pytest.fixture
def ring():
    return Sprite.from_text(RING)


def stroke(tool: Tool, sprite: Sprite, cells: list, colour=2):
    """Press on the first cell, drag through the rest, and let go."""
    tool.press(sprite, cells[0], colour)
    for cell in cells[1:]:
        tool.drag(sprite, cell)
    return tool.release(sprite)


def test_shapes():
    assert cells_between((0, 0), (3, 1)) == [(0, 0), (1, 0), (2, 1), (3, 1)]
    assert sorted(box((2, 2), (0, 0))) == [
        (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2),
    ]  # fmt: skip


def test_flood_stops_at_other_colours_and_at_the_edge(ring):
    assert flood(ring, (2, 2)) == {(2, 2)}
    assert len(flood(ring, (1, 1))) == 8
    assert len(flood(ring, (0, 0))) == 16


def test_flood_is_not_upset_by_a_big_empty_sprite():
    assert len(flood(Sprite(200, 200), (0, 0))) == 40_000


def test_a_tool_changes_nothing_until_it_lets_go(ring):
    pencil = Pencil()
    pencil.press(ring, (0, 0), 2)
    pencil.drag(ring, (4, 0))
    assert pencil.changes == dict.fromkeys([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], 2)
    assert ring == Sprite.from_text(RING)

    command = pencil.release(ring)
    assert isinstance(command, Paint)
    assert str(command) == "Pencil"
    assert pencil.changes == {}
    command.do(ring)
    assert ring.to_text().splitlines()[1] == "22222"


def test_the_eraser_is_a_pencil_that_ignores_the_colour(ring):
    eraser = Eraser()
    assert isinstance(eraser, Pencil)
    command = stroke(eraser, ring, [(1, 1), (3, 1)], colour=6)
    assert command.after == {(1, 1): None, (2, 1): None, (3, 1): None}
    assert str(command) == "Eraser"


def test_rubbing_out_nothing_is_no_command_at_all(ring):
    assert stroke(Eraser(), ring, [(0, 0), (4, 0)]) is None


def test_a_shape_follows_the_pointer_and_only_the_last_one_counts(ring):
    line = Line()
    line.press(ring, (0, 0), 3)
    line.drag(ring, (4, 4))
    line.drag(ring, (0, 4))
    assert line.changes == dict.fromkeys([(0, y) for y in range(5)], 3)

    command = stroke(Box(), ring, [(0, 0), (2, 2), (4, 4)], colour=3)
    assert len(command.after) == 16


def test_shapes_may_run_off_the_edge(ring):
    command = stroke(Line(), ring, [(3, 0), (9, 0)])
    assert command.after == {(3, 0): 2, (4, 0): 2}


def test_the_bucket(ring):
    command = stroke(Bucket(), ring, [(2, 2)], colour=4)
    assert command.after == {(2, 2): 4}
    assert stroke(Bucket(), ring, [(1, 1)], colour=1) is None


def test_the_picker_reports_and_draws_nothing(ring):
    picked = []
    picker = Picker(on_pick=picked.append)
    assert stroke(picker, ring, [(1, 1), (2, 2), (7, 7)]) is None
    assert picked == [1, None]


def test_the_family():
    with pytest.raises(TypeError, match="abstract"):
        ShapeTool()
    assert [kind.__name__ for kind in Line.__mro__] == [
        "Line", "ShapeTool", "Tool", "ABC", "object",
    ]  # fmt: skip
