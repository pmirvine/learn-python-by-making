import pygame
import pytest

import beeb


def test_drawing_before_mode_is_a_clear_error():
    beeb.screen._canvas = None
    with pytest.raises(RuntimeError, match="call beeb.mode"):
        beeb.clg()


def test_bad_mode():
    with pytest.raises(ValueError, match="Bad MODE"):
        beeb.mode(3)


def test_mode_starts_black_with_white_ink(mode2):
    assert beeb.point(640, 512) == 0
    beeb.plot(69, 640, 512)
    assert beeb.point(640, 512) == 7


def test_draw_joins_the_cursor_to_the_new_point(mode2):
    beeb.gcol(0, 3)
    beeb.move(0, 0)
    beeb.draw(1279, 0)
    assert [beeb.point(x, 0) for x in (0, 640, 1279)] == [3, 3, 3]
    assert beeb.point(640, 8) == 0


def test_lines_continue_from_where_the_last_one_ended(mode2):
    beeb.move(0, 0)
    beeb.draw(0, 1000)
    beeb.draw(1000, 1000)
    assert beeb.point(500, 1000) == 7


def test_background_colour_and_clg(mode2):
    beeb.gcol(0, 129)
    beeb.clg()
    assert beeb.point(100, 100) == 1


def test_colour_numbers_wrap_to_the_mode():
    beeb.mode(1)
    beeb.gcol(0, 6)
    beeb.plot(69, 100, 100)
    assert beeb.point(100, 100) == 2


def test_relative_plotting(mode2):
    beeb.move(400, 400)
    beeb.plot(1, 200, 0)
    assert beeb.point(500, 400) == 7
    beeb.plot(0, 0, 100)
    beeb.plot(1, -200, 0)
    assert beeb.point(500, 500) == 7


def test_plot_85_fills_a_triangle_from_the_last_two_points(mode2):
    beeb.gcol(0, 2)
    beeb.move(200, 200)
    beeb.move(1000, 200)
    beeb.plot(85, 600, 800)
    assert beeb.point(600, 400) == 2
    assert beeb.point(210, 790) == 0


def test_plotting_in_the_background_colour_rubs_out(mode2):
    beeb.move(0, 512)
    beeb.draw(1279, 512)
    beeb.move(0, 512)
    beeb.plot(7, 1279, 512)
    assert beeb.point(640, 512) == 0


def test_point_off_screen(mode2):
    assert beeb.point(-1, 0) == -1
    assert beeb.point(0, 1024) == -1


def test_unsupported_plot_codes(mode2):
    with pytest.raises(ValueError, match="PLOT 101"):
        beeb.plot(101, 0, 0)
    with pytest.raises(NotImplementedError):
        beeb.plot(6, 0, 0)


def test_closing_the_window_ends_the_program(mode2):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    with pytest.raises(SystemExit):
        beeb.vsync()


def test_typed_keys_queue_up_for_inkey(mode2):
    for letter in "hi":
        pygame.event.post(
            pygame.event.Event(pygame.KEYDOWN, key=ord(letter), unicode=letter)
        )
    beeb.vsync()
    assert [beeb.inkey(), beeb.inkey(), beeb.inkey()] == ["h", "i", ""]


def test_screenshot(mode2, tmp_path):
    beeb.gcol(0, 1)
    beeb.plot(69, 0, 0)
    beeb.screenshot(str(tmp_path / "shot.png"))
    image = pygame.image.load(tmp_path / "shot.png")
    assert image.get_size() == (640, 512)
    assert image.get_at((0, 511))[:3] == (255, 0, 0)


def test_the_canvas_is_the_size_of_the_mode(mode2):
    assert beeb.canvas().get_size() == (160, 256)


def test_what_is_drawn_is_on_the_canvas(mode2):
    beeb.gcol(0, 1)
    beeb.plot(69, 0, 0)
    assert beeb.canvas().get_at_mapped((0, 255)) == 1
