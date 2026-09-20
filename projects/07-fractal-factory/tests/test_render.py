import pytest
from PIL import Image

from fractals import gradient, mandelbrot, render
from fractals.cli import main, parse_size

GREY = gradient((0, 0, 0), (255, 255, 255))


def test_render_makes_an_image_of_the_size_asked_for():
    image = render(mandelbrot(20), GREY, size=(12, 8), centre=-0.5 + 0j)
    assert image.size == (12, 8)
    assert image.getpixel((6, 4)) == (255, 255, 255)
    assert image.getpixel((0, 0)) != (255, 255, 255)


def test_render_passes_each_pixel_its_own_point():
    seen = []

    def spy(point: complex) -> float:
        seen.append(point)
        return 0.0

    render(spy, GREY, size=(4, 2), centre=10 + 10j, width=4.0)
    assert len(seen) == 8
    assert seen[0] == 8 + 11j
    assert seen[-1] == 11 + 10j


def test_size_and_the_rest_must_be_given_by_name():
    with pytest.raises(TypeError, match="positional"):
        render(mandelbrot(), GREY, (12, 8))


def test_parse_size():
    assert parse_size("640x480") == (640, 480)
    assert parse_size("32X16") == (32, 16)


def test_the_command_saves_a_picture(tmp_path, capsys):
    target = tmp_path / "tiny.png"
    main(
        [
            "julia",
            "--size",
            "16x12",
            "--c=-0.4+0.6j",
            "--palette",
            "beeb",
            "-o",
            str(target),
        ]
    )
    assert Image.open(target).size == (16, 12)
    assert "Saved" in capsys.readouterr().out


def test_a_bad_size_is_reported_politely(capsys):
    with pytest.raises(SystemExit):
        main(["plasma", "--size", "big"])
    assert "isn't a size such as 640x480" in capsys.readouterr().err
