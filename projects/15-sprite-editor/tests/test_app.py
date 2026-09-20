import logging

import pygame
import pytest

from sprite_editor.app import SIZE, App, open_sprite
from sprite_editor.sprite import Sprite
from sprite_editor.widgets import PALETTE, Canvas


@pytest.fixture
def app(tmp_path):
    pygame.init()
    window = pygame.display.set_mode(SIZE)
    yield App(window, Sprite(16, 16), tmp_path / "test.sprite")
    pygame.quit()


def event(kind: int, **details) -> pygame.event.Event:
    return pygame.event.Event(kind, **details)


def press(app: App, key: int, mod: int = 0) -> None:
    assert app.handle(event(pygame.KEYDOWN, key=key, mod=mod))


def middle_of(app: App, cell: tuple[int, int]) -> tuple[int, int]:
    zoom = app.canvas.zoom
    return (
        app.canvas.rect.left + cell[0] * zoom + zoom // 2,
        app.canvas.rect.top + cell[1] * zoom + zoom // 2,
    )


def drag(app: App, *cells: tuple[int, int]) -> None:
    app.handle(event(pygame.MOUSEBUTTONDOWN, button=1, pos=middle_of(app, cells[0])))
    for cell in cells[1:]:
        app.handle(event(pygame.MOUSEMOTION, pos=middle_of(app, cell)))
    app.handle(event(pygame.MOUSEBUTTONUP, button=1, pos=middle_of(app, cells[-1])))


def click(app: App, label: str) -> None:
    button = next(button for button in app.buttons if button.label == label)
    app.handle(event(pygame.MOUSEBUTTONDOWN, button=1, pos=button.rect.center))
    app.handle(event(pygame.MOUSEBUTTONUP, button=1, pos=button.rect.center))


def test_the_canvas_knows_which_cell_is_where():
    canvas = Canvas(pygame.Rect(16, 16, 400, 400), Sprite(16, 16))
    assert canvas.zoom == 25
    assert canvas.cell_at((16, 16)) == (0, 0)
    assert canvas.cell_at((40, 41)) == (0, 1)
    assert canvas.cell_at((15, 16)) == (-1, 0)


def test_a_drag_is_one_command_and_one_undo(app):
    drag(app, (2, 2), (5, 2), (5, 6))
    assert len(app.sprite.pixels) == 8
    assert [str(command) for command in app.history.done] == ["Pencil"]
    press(app, pygame.K_z, pygame.KMOD_CTRL)
    assert app.sprite.pixels == {}


def test_nothing_is_changed_until_the_button_comes_up(app):
    app.handle(event(pygame.MOUSEBUTTONDOWN, button=1, pos=middle_of(app, (2, 2))))
    app.handle(event(pygame.MOUSEMOTION, pos=middle_of(app, (9, 2))))
    assert app.sprite.pixels == {}
    app.draw()
    assert app.window.get_at(middle_of(app, (6, 2)))[:3] == PALETTE[7]


def test_every_button_does_what_it_says(app):
    click(app, "colour 1")
    click(app, "Line")
    drag(app, (0, 0), (3, 0))
    assert app.sprite[3, 0] == 1

    click(app, "Flip")
    assert app.sprite[15, 0] == 1
    click(app, "Undo")
    click(app, "Undo")
    assert app.sprite.pixels == {}
    click(app, "Redo")
    assert app.sprite[0, 0] == 1


def test_each_swatch_chooses_its_own_colour_and_not_the_last_one(app):
    chosen = []
    for label in ("colour None", "colour 0", "colour 3", "colour 7"):
        click(app, label)
        chosen.append(app.colour)
    assert chosen == [None, 0, 3, 7]
    lit = [button.label for button in app.buttons if button.is_on()]
    assert lit == ["colour 7", "Pencil"]


def test_the_keys(app):
    press(app, pygame.K_4)
    press(app, pygame.K_f)
    assert (app.colour, app.tool.name) == (4, "Fill")
    drag(app, (8, 8))
    assert len(app.sprite.pixels) == 256

    press(app, pygame.K_PERIOD)
    press(app, pygame.K_b)
    drag(app, (0, 0), (15, 15))
    assert len(app.sprite.pixels) == 196

    press(app, pygame.K_z, pygame.KMOD_META)
    press(app, pygame.K_z, pygame.KMOD_CTRL)
    press(app, pygame.K_z, pygame.KMOD_CTRL | pygame.KMOD_SHIFT)
    press(app, pygame.K_y, pygame.KMOD_CTRL)
    assert len(app.sprite.pixels) == 196
    press(app, pygame.K_z)  # the letter by itself is nothing
    press(app, pygame.K_F5)
    assert len(app.history.done) == 2


def test_the_picker_calls_back(app):
    press(app, pygame.K_2)
    drag(app, (3, 3))
    press(app, pygame.K_7)
    press(app, pygame.K_p)
    assert app.tool.name == "Pencil"
    click(app, "Pick")
    drag(app, (3, 3))
    assert app.colour == 2
    assert len(app.history.done) == 1


def test_arrows_shift_and_h_flips(app):
    drag(app, (0, 0))
    press(app, pygame.K_LEFT)
    press(app, pygame.K_UP)
    assert app.sprite.pixels == {(15, 15): 7}
    press(app, pygame.K_h)
    assert app.sprite.pixels == {(0, 15): 7}


def test_saving_and_the_star(app, caplog):
    caplog.set_level(logging.INFO)
    assert not app.changed
    drag(app, (1, 1))
    assert app.changed
    press(app, pygame.K_s, pygame.KMOD_CTRL)
    assert not app.changed
    assert Sprite.load(app.path) == app.sprite
    assert app.message == "Saved test.sprite"
    assert "Saved" in caplog.text

    press(app, pygame.K_z, pygame.KMOD_CTRL)
    assert app.changed
    press(app, pygame.K_y, pygame.KMOD_CTRL)
    assert not app.changed


def test_a_save_that_fails_is_logged_and_shown(app, caplog):
    app.path = app.path.parent / "no such folder" / "test.sprite"
    click(app, "Save")
    assert app.message.startswith("Couldn't save")
    assert [record.levelname for record in caplog.records] == ["WARNING"]


def test_opening(tmp_path):
    assert open_sprite(tmp_path / "new.sprite", 8) == Sprite(8, 8)
    bad = tmp_path / "bad.sprite"
    bad.write_text("sprite 2 2\n..\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="there are 1 rows, and not 2"):
        open_sprite(bad, 8)


def test_quitting_and_drawing(app):
    app.draw()
    assert not app.handle(event(pygame.QUIT))
