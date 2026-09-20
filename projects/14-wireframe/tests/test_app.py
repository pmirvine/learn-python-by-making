import pygame
import pytest

from wireframe.app import DRIFT, SIZE, App
from wireframe.matrix import IDENTITY
from wireframe.model import hangar
from wireframe.view import Style

STILL = (0.0, 0.0, 0.0)
DART = """
name = "Paper dart"
points = [[0, 0, 9], [-3, 0, -3], [3, 0, -3], [0, 2, -3]]

[[faces]]
points = [0, 2, 1]
colour = "COLOUR"
"""


@pytest.fixture
def app():
    pygame.init()
    app = App(pygame.display.set_mode(SIZE), hangar())
    app.orientation = IDENTITY
    app.drifting = False
    yield app
    pygame.quit()


def press(app: App, key: int) -> None:
    assert app.handle(pygame.event.Event(pygame.KEYDOWN, key=key))


def lit(app: App) -> int:
    """Count the pixels that aren't black."""
    app.frame(0.0, STILL)
    black = pygame.mask.from_threshold(app.view.window, (0, 0, 0), (1, 1, 1))
    black.invert()
    return black.count()


def test_tab_goes_round_the_hangar(app):
    names = [ship.name for ship in app.ships]
    seen = []
    for _ in names:
        seen.append(app.ship.name)
        press(app, pygame.K_TAB)
    assert seen == names
    assert app.ship.name == names[0]


def test_h_goes_round_the_styles(app):
    seen = []
    for _ in range(4):
        seen.append(app.style)
        press(app, pygame.K_h)
    assert seen == [Style.WIRES, Style.HIDDEN, Style.SOLID, Style.WIRES]


def test_holding_a_key_turns_the_ship_and_time_matters(app):
    app.frame(0.5, (90.0, 0.0, 0.0))
    nose = app.orientation @ app.ship.points[0]
    assert abs(nose) == pytest.approx(abs(app.ship.points[0]))
    assert app.orientation != IDENTITY
    app.frame(0.5, (-90.0, 0.0, 0.0))
    for row, expected in zip(app.orientation.rows, IDENTITY.rows, strict=True):
        assert row == pytest.approx(expected)


def test_left_alone_it_drifts_unless_told_not_to(app):
    app.frame(1.0, STILL)
    assert app.orientation == IDENTITY
    press(app, pygame.K_SPACE)
    app.frame(1.0, STILL)
    assert app.orientation != IDENTITY
    assert any(DRIFT)


def test_plus_and_minus_move_the_eye_within_limits(app):
    start = app.distance
    press(app, pygame.K_EQUALS)
    assert app.distance < start
    for _ in range(100):
        press(app, pygame.K_MINUS)
    assert app.distance == 20 * app.ship.radius


def test_hidden_lines_draw_less_and_solid_draws_more(app):
    wires = lit(app)
    press(app, pygame.K_h)
    hidden = lit(app)
    press(app, pygame.K_h)
    solid = lit(app)
    assert 0 < hidden < wires < solid


def test_a_dropped_ship_joins_the_hangar(app, tmp_path):
    path = tmp_path / "dart.toml"
    path.write_text(DART.replace("COLOUR", "tomato"), encoding="utf-8")
    count = len(app.ships)
    app.handle(pygame.event.Event(pygame.DROPFILE, file=str(path)))
    assert len(app.ships) == count + 1
    assert app.ship.name == "Paper dart"
    assert app.message == ""


@pytest.mark.parametrize(
    ("text", "complaint"),
    [
        (DART.replace("COLOUR", "tomatoe"), "dart.toml: "),
        (DART.replace("[0, 2, 1]", "[0, 2, 7]"), "no such point"),
        ("Dear Sir,", "isn't TOML"),
    ],
)
def test_a_bad_file_is_reported_and_changes_nothing(app, tmp_path, text, complaint):
    path = tmp_path / "dart.toml"
    path.write_text(text, encoding="utf-8")
    before = [ship.name for ship in app.ships]
    app.handle(pygame.event.Event(pygame.DROPFILE, file=str(path)))
    assert [ship.name for ship in app.ships] == before
    assert complaint in app.message


def test_quitting(app):
    assert not app.handle(pygame.event.Event(pygame.QUIT))
