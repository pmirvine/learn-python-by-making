import pytest

from wireframe.model import Face, ModelError, hangar, load, parse
from wireframe.vec3 import Vec3

TENT = """
name = "Tent"
points = [[0, 1, 0], [-1, 0, 1], [1, 0, 1], [0, 0, -1.5]]

[[faces]]
points = [0, 1, 2]
colour = "red"

[[faces]]
points = [0, 2, 3]
"""


def test_a_ship():
    tent = parse(TENT)
    assert tent.name == "Tent"
    assert tent.points[3] == Vec3(0, 0, -1.5)
    assert tent.faces == (Face((0, 1, 2), "red"), Face((0, 2, 3), "white"))
    assert tent.radius == 1.5


def test_loading_from_a_file(tmp_path):
    path = tmp_path / "tent.toml"
    path.write_text(TENT, encoding="utf-8")
    assert load(path) == parse(TENT)


@pytest.mark.parametrize(
    ("old", "new", "complaint"),
    [
        ('name = "Tent"', "name = Tent", "isn't TOML"),
        ('name = "Tent"', "name = 7", "needs a name"),
        ("[0, 1, 0]", "[0, 1]", "point 0 should be three numbers"),
        ("[0, 1, 0]", '[0, "1", 0]', "point 0 should be three numbers"),
        ("[0, 2, 3]", "[0, 2]", "face 1 needs points"),
        ("[0, 2, 3]", "[0, 2, 4]", "face 1 uses point 4"),
        ('colour = "red"', 'color = "red"', "face 0 needs points"),
        ('colour = "red"', "colour = 3", "face 0 needs points"),
    ],
)
def test_bad_ships_are_reported(old, new, complaint):
    assert old in TENT
    with pytest.raises(ModelError, match=complaint):
        parse(TENT.replace(old, new))


def test_the_hangar_is_in_order_and_every_face_has_a_colour_and_corners():
    ships = hangar()
    names = [ship.name for ship in ships]
    assert names == sorted(names)
    assert "Dart" in names
    for ship in ships:
        assert all(len(face.points) >= 3 for face in ship.faces)
