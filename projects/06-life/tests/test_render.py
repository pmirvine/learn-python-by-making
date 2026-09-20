from life import PATTERNS, parse, render
from life.cli import main, parse_arguments


def test_render_draws_each_cell_two_characters_wide():
    picture = render({(0, 0), (2, 1)}, width=3, height=2)
    assert picture == "██    \n    ██"


def test_render_shows_only_the_window_asked_for():
    glider = parse(PATTERNS["glider"])
    assert render(glider, 2, 2) == "  ██\n    "
    assert render({(-1, -1), (99, 99)}, 2, 1) == "    "


def test_arguments_have_sensible_defaults():
    args = parse_arguments([])
    assert (args.pattern, args.generations, args.fps) == ("soup", None, 10)


def test_arguments_can_be_given():
    args = parse_arguments(["glider", "-g", "5", "--fps", "2.5", "--seed", "9"])
    assert (args.pattern, args.generations, args.fps, args.seed) == (
        "glider",
        5,
        2.5,
        9,
    )


def test_the_program_runs_and_reports_each_generation(capsys):
    main(["blinker", "--generations", "3", "--fps", "1000"])
    out = capsys.readouterr().out
    assert "Generation 0, population 3" in out
    assert "Generation 2, population 3" in out
    assert "Generation 3" not in out
