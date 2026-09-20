import pygame
import pytest

from logo.app import SIZE, WELCOME, App, draw_to_svg, is_complete


@pytest.fixture
def app():
    pygame.init()
    yield App(pygame.display.set_mode(SIZE))
    pygame.quit()


def type_in(app: App, *lines: str) -> None:
    for line in lines:
        app.handle(pygame.event.Event(pygame.TEXTINPUT, text=line))
        app.handle(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN))


def press(app: App, key: int) -> None:
    assert app.handle(pygame.event.Event(pygame.KEYDOWN, key=key))


@pytest.mark.parametrize(
    ("text", "complete"),
    [
        ("fd 100", True),
        ("repeat 4 [fd 100", False),
        ("repeat 4 [fd 100\nrt 90]", True),
        ("to square :size", False),
        ("to square :size\nrepeat 4 [fd :size rt 90]\nend", True),
        ('print "to', True),
        ("fd 100 ]", True),
        ("fd £", True),
    ],
)
def test_is_there_more_to_come(text, complete):
    assert is_complete(text) is complete


def test_typing_a_line_draws_on_the_canvas(app):
    type_in(app, "setpc 1 fd 100")
    assert app.output == [WELCOME, "? setpc 1 fd 100"]
    middle = app.canvas.to_screen((0, 50))
    assert app.canvas.surface.get_at(middle)[:3] == (255, 0, 0)


def test_backspace_and_escape(app):
    app.handle(pygame.event.Event(pygame.TEXTINPUT, text="fd 1000"))
    press(app, pygame.K_BACKSPACE)
    assert app.typed == "fd 100"
    press(app, pygame.K_ESCAPE)
    assert app.typed == ""


def test_a_procedure_can_be_typed_over_several_lines(app):
    type_in(app, "to square :size", "repeat 4 [fd :size rt 90]")
    assert app.pending
    assert "SQUARE" not in app.logo.procedures
    type_in(app, "end", "square 50")
    assert not app.pending
    assert app.output[-4:] == [
        "? to square :size",
        "> repeat 4 [fd :size rt 90]",
        "> end",
        "? square 50",
    ]
    assert app.canvas.surface.get_at(app.canvas.to_screen((25, 50)))[:3] != (0, 0, 0)


def test_mistakes_are_shown_and_do_no_harm(app):
    type_in(app, "jump 50", "fd 10")
    assert app.output[-3:] == ["? jump 50", "I don't know how to JUMP", "? fd 10"]
    assert app.logo.turtle.y == 10


def test_print_and_help_come_out_in_the_window(app):
    type_in(app, "print 6 * 7")
    assert app.output[-1] == "42"
    type_in(app, "help")
    assert any(line.startswith("REPEAT 4 [FD 50 RT 90]") for line in app.output)


def test_the_arrows_bring_back_earlier_lines(app):
    type_in(app, "fd 10", "rt 90")
    press(app, pygame.K_UP)
    assert app.typed == "rt 90"
    press(app, pygame.K_UP)
    press(app, pygame.K_UP)
    assert app.typed == "fd 10"
    press(app, pygame.K_DOWN)
    press(app, pygame.K_DOWN)
    assert app.typed == ""


def test_it_draws_itself_and_quits(app):
    type_in(app, "rt 30 fd 50")
    app.draw()
    assert not app.handle(pygame.event.Event(pygame.QUIT))


def test_a_program_can_be_drawn_with_no_window_at_all(tmp_path, capsys):
    program = tmp_path / "square.logo"
    program.write_text("repeat 4 [fd 100 rt 90]", encoding="utf-8")
    draw_to_svg(program, tmp_path / "square.svg")
    assert (tmp_path / "square.svg").read_text(encoding="utf-8").count("<line") == 4
    assert "with 4 lines in it" in capsys.readouterr().out
