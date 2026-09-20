"""The test that fails with the colleague's History, and passes with the mended one."""

from history import History

from sprite_editor.commands import Paint
from sprite_editor.sprite import Sprite


def test_doing_something_new_forgets_what_was_undone():
    sprite = Sprite(5, 5)
    history = History(sprite)
    history.perform(Paint("Red line", sprite, {(x, 2): 1 for x in range(5)}))
    history.undo()
    history.perform(Paint("Blue line", sprite, {(2, y): 4 for y in range(5)}))

    history.redo()

    assert history.undone == []
    assert sprite.pixels == {(2, y): 4 for y in range(5)}
