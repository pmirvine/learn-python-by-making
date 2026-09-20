import pytest

from logo.turtle import Recorder, SvgCanvas, Turtle


def test_forward_goes_the_way_the_turtle_is_facing():
    turtle = Turtle(Recorder())
    turtle.turn(90)
    turtle.forward(10)
    assert (turtle.x, turtle.y) == pytest.approx((10, 0))
    turtle.turn(90)
    turtle.forward(10)
    assert (turtle.x, turtle.y) == pytest.approx((10, -10))


def test_headings_wrap_round():
    turtle = Turtle(Recorder())
    turtle.turn(-90)
    assert turtle.heading == 270
    turtle.turn(450)
    assert turtle.heading == 0


def test_an_svg_has_a_line_for_each_line_with_y_the_other_way_up(tmp_path):
    canvas = SvgCanvas(size=200)
    turtle = Turtle(canvas, colour=1)
    turtle.forward(50)
    path = tmp_path / "line.svg"
    canvas.save(path)
    svg = path.read_text(encoding="utf-8")
    assert svg.startswith("<svg xmlns=")
    assert '<line x1="100.0" y1="100.0" x2="100.0" y2="50.0" stroke="red"/>' in svg
