import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from plotter import Plot

SVG = "{http://www.w3.org/2000/svg}"


def parsed(plot: Plot) -> ET.Element:
    """Return the picture as a tree, which also proves that it's well-formed XML."""
    return ET.fromstring(plot.svg())


@pytest.fixture
def plot(tmp_path: Path) -> Plot:
    return Plot(tmp_path / "test.svg", width=100, height=100)


def test_the_origin_is_at_the_bottom_left(plot):
    plot.move(0, 0)
    plot.draw(100, 25)
    (path,) = parsed(plot).iter(f"{SVG}path")
    assert path.get("d") == "M0.0 100.0 L100.0 75.0"


def test_draws_join_up_into_one_stroke_until_the_pen_moves_or_changes(plot):
    plot.move(0, 0)
    plot.draw(10, 0)
    plot.draw(10, 10)
    plot.move(50, 50)
    plot.draw(60, 60)
    plot.pen("red", width=5)
    plot.draw(70, 50)
    paths = list(parsed(plot).iter(f"{SVG}path"))
    assert [path.get("d", "").count("L") for path in paths] == [2, 1, 1]
    assert [path.get("stroke") for path in paths] == ["white", "white", "red"]
    assert paths[2].get("stroke-width") == "5"
    assert paths[2].get("d", "").startswith("M60.0 40.0")


def test_a_move_by_itself_draws_nothing(plot):
    plot.move(10, 10)
    plot.move(20, 20)
    assert list(parsed(plot).iter(f"{SVG}path")) == []


def test_awkward_characters_survive_in_labels_and_titles(tmp_path):
    plot = Plot(tmp_path / "t.svg", title="Fish & <Chips>")
    plot.label(10, 10, 'if x < 3 & y > "4"')
    tree = parsed(plot)
    assert tree.findtext(f"{SVG}title") == "Fish & <Chips>"
    assert tree.findtext(f"{SVG}text") == 'if x < 3 & y > "4"'


def test_a_group_turns_what_is_inside_it_and_nothing_else(plot):
    plot.move(0, 0)
    plot.draw(10, 10)
    with plot.turned(90, about=(50, 50)):
        plot.move(50, 50)
        plot.draw(60, 50)
        plot.label(50, 50, "sideways")
    plot.draw(20, 20)
    tree = parsed(plot)
    (group,) = tree.iter(f"{SVG}g")
    assert group.get("transform") == "rotate(-90 50 50)"
    assert [child.tag for child in group] == [f"{SVG}path", f"{SVG}text"]
    assert len(list(tree.iter(f"{SVG}path"))) == 3


def test_groups_close_even_when_something_goes_wrong_inside(plot):
    with pytest.raises(ZeroDivisionError), plot.turned(45, about=(0, 0)):
        plot.draw(1 / 0, 0)
    assert len(plot.open_groups) == 1


def test_the_file_is_written_when_the_with_finishes(tmp_path):
    path = tmp_path / "square.svg"
    with Plot(path) as plot:
        plot.draw(100, 100)
        assert not path.exists()
    assert ET.parse(path).getroot().tag == f"{SVG}svg"


def test_and_not_if_it_went_wrong(tmp_path):
    path = tmp_path / "broken.svg"
    with pytest.raises(ValueError, match="oops"), Plot(path) as plot:
        plot.draw(100, 100)
        raise ValueError("oops")
    assert not path.exists()


def test_a_picture_can_draw_itself_one_stroke_after_another(tmp_path):
    plot = Plot(tmp_path / "t.svg", seconds=10)
    plot.draw(300, 0)
    plot.move(0, 100)
    plot.draw(100, 100)
    first, second = parsed(plot).iter(f"{SVG}path")
    assert first.get("style") == "animation-delay:0.00s;animation-duration:7.50s"
    assert second.get("style") == "animation-delay:7.50s;animation-duration:2.50s"
    assert "@keyframes" in (parsed(plot).findtext(f"{SVG}style") or "")


def test_a_still_picture_has_no_animation(plot):
    plot.draw(10, 10)
    assert (parsed(plot).findtext(f"{SVG}style") or "").strip() == ""
