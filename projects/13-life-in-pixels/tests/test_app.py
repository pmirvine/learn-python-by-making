import pygame
import pytest
from life import PATTERNS, parse

from pixel_life.app import App, cells_between
from pixel_life.view import ALIVE, BACKGROUND


@pytest.fixture
def app():
    pygame.init()
    window = pygame.display.set_mode((640, 480))
    app = App(window)
    app.simulation.load(set())
    app.camera.x = app.camera.y = 0.0
    app.camera.zoom = 8.0
    return app


def event(kind: int, **details) -> pygame.event.Event:
    return pygame.event.Event(kind, **details)


@pytest.mark.parametrize(
    ("start", "end", "cells"),
    [
        ((0, 0), (0, 0), [(0, 0)]),
        ((0, 0), (3, 0), [(0, 0), (1, 0), (2, 0), (3, 0)]),
        ((2, 2), (0, 0), [(2, 2), (1, 1), (0, 0)]),
        ((0, 0), (4, 2), [(0, 0), (1, 0), (2, 1), (3, 2), (4, 2)]),
    ],
)
def test_cells_between(start, end, cells):
    assert cells_between(start, end) == cells


def test_it_starts_with_the_gun_in_the_middle_of_the_window():
    pygame.init()
    app = App(pygame.display.set_mode((640, 480)))
    assert len(app.simulation.live) == 36
    assert app.camera.cell_at((320, 240)) == (17, 4)


def test_dragging_paints_a_line_with_no_gaps(app):
    app.handle(event(pygame.MOUSEBUTTONDOWN, button=1, pos=(4, 4)))
    app.handle(event(pygame.MOUSEMOTION, pos=(44, 4), rel=(40, 0), buttons=(1, 0, 0)))
    app.handle(event(pygame.MOUSEBUTTONUP, button=1, pos=(44, 4)))
    assert app.simulation.live == {(x, 0) for x in range(6)}

    app.handle(event(pygame.MOUSEMOTION, pos=(44, 44), rel=(0, 40), buttons=(0, 0, 0)))
    assert len(app.simulation.live) == 6


def test_starting_on_a_live_cell_rubs_out(app):
    app.simulation.load({(0, 0), (1, 0), (2, 0)})
    app.handle(event(pygame.MOUSEBUTTONDOWN, button=1, pos=(4, 4)))
    app.handle(event(pygame.MOUSEMOTION, pos=(20, 4), rel=(16, 0), buttons=(1, 0, 0)))
    assert app.simulation.live == set()


def test_the_right_button_drags_the_universe(app):
    before = app.camera.cell_at((100, 100))
    app.handle(
        event(pygame.MOUSEMOTION, pos=(140, 100), rel=(40, 0), buttons=(0, 0, 1))
    )
    assert app.camera.cell_at((140, 100)) == before


def test_keys(app):
    app.simulation.load(parse(PATTERNS["blinker"]))
    assert app.handle(event(pygame.KEYDOWN, key=pygame.K_SPACE))
    assert app.simulation.running
    app.handle(event(pygame.KEYDOWN, key=pygame.K_n))
    assert app.simulation.generation == 1
    app.handle(event(pygame.KEYDOWN, key=pygame.K_EQUALS))
    assert app.simulation.speed == 20
    app.handle(event(pygame.KEYDOWN, key=pygame.K_5))
    assert app.simulation.live == parse(PATTERNS["glider"])
    app.handle(event(pygame.KEYDOWN, key=pygame.K_r))
    assert len(app.simulation.live) > 500
    app.handle(event(pygame.KEYDOWN, key=pygame.K_c))
    assert app.simulation.live == set()
    assert not app.handle(event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    assert not app.handle(event(pygame.QUIT))


def test_a_dropped_file_is_loaded(app, tmp_path):
    file = tmp_path / "glider.rle"
    file.write_text("x = 3, y = 3\nbob$2bo$3o!\n", encoding="utf-8")
    app.handle(event(pygame.DROPFILE, file=str(file)))
    assert app.simulation.live == parse(PATTERNS["glider"])
    assert app.message == "Loaded glider.rle: 5 cells."


def test_a_dropped_file_of_rubbish_is_reported_and_changes_nothing(app, tmp_path):
    file = tmp_path / "shopping.txt"
    file.write_text("eggs, milk, bread", encoding="utf-8")
    app.simulation.load({(1, 1)})
    app.handle(event(pygame.DROPFILE, file=str(file)))
    assert app.message.startswith("Couldn't load shopping.txt")
    assert app.simulation.live == {(1, 1)}


def test_only_the_cells_in_view_are_drawn_and_in_the_right_places(app):
    app.simulation.load({(0, 0), (10, 5), (-50, -50), (5000, 5000)})
    app.frame(0.0)
    assert app.window.get_at((3, 3))[:3] == ALIVE
    assert app.window.get_at((83, 43))[:3] == ALIVE
    assert app.window.get_at((300, 300))[:3] == BACKGROUND
