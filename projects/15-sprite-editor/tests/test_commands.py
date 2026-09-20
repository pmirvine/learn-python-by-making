import pytest

from sprite_editor.commands import Command, Flip, History, Paint, Shift
from sprite_editor.sprite import Sprite

ARROW = """\
sprite 4 3
.1..
1111
.1..
"""


@pytest.fixture
def arrow():
    return Sprite.from_text(ARROW)


def test_a_command_has_to_say_how_to_do_and_undo():
    class Half(Command):
        def do(self, sprite):
            sprite.pixels.clear()

    with pytest.raises(TypeError, match="abstract method 'undo'"):
        Half()


def test_paint_remembers_what_was_there(arrow):
    paint = Paint("Dot", arrow, {(0, 0): 3, (1, 0): None, (9, 9): 3})
    assert paint.before == {(0, 0): None, (1, 0): 1}
    paint.do(arrow)
    assert arrow.to_text().splitlines()[1] == "3..."
    paint.undo(arrow)
    assert arrow == Sprite.from_text(ARROW)


def test_paint_that_changes_nothing_is_false(arrow):
    assert not Paint("Nothing", arrow, {(0, 0): None, (1, 0): 1})
    assert Paint("Something", arrow, {(0, 0): 1})


@pytest.mark.parametrize("command", [Flip(), Shift(1, 0), Shift(-3, 2)], ids=str)
def test_whatever_is_done_can_be_undone(arrow, command):
    command.do(arrow)
    assert arrow != Sprite.from_text(ARROW)
    command.undo(arrow)
    assert arrow == Sprite.from_text(ARROW)


def test_flip_and_shift(arrow):
    Flip().do(arrow)
    assert arrow.to_text() == "sprite 4 3\n..1.\n1111\n..1.\n"
    Shift(2, 1).do(arrow)
    assert arrow.to_text() == "sprite 4 3\n1...\n1...\n1111\n"
    assert str(Shift(2, -1)) == "Shift +2, -1"


def test_history_goes_back_and_forward(arrow):
    history = History(arrow)
    history.perform(Flip())
    history.perform(Paint("Dot", arrow, {(0, 0): 7}))
    assert arrow[0, 0] == 7

    history.undo()
    history.undo()
    assert arrow == Sprite.from_text(ARROW)
    history.undo()  # and once more, which is harmless
    assert str(history) == "0 done, 2 undone"

    history.redo()
    history.redo()
    history.redo()
    assert arrow[0, 0] == 7
    assert [str(command) for command in history.done] == ["Flip", "Dot"]


def test_doing_something_new_forgets_what_was_undone(arrow):
    history = History(arrow)
    history.perform(Paint("Red", arrow, {(0, 0): 1}))
    history.undo()
    history.perform(Paint("Blue", arrow, {(0, 0): 4}))
    history.redo()
    assert arrow[0, 0] == 4
    assert history.undone == []


def test_the_history_keeps_a_diary(arrow, caplog):
    caplog.set_level("DEBUG", logger="sprite_editor.commands")
    history = History(arrow)
    history.perform(Flip())
    history.undo()
    history.undo()
    assert caplog.messages == [
        "Did Flip. 1 done, 0 undone",
        "Undid Flip. 0 done, 1 undone",
        "Nothing to undo",
    ]
