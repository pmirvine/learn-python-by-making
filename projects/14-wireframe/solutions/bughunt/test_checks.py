from pathlib import Path

from checks import inside_out

from wireframe.model import hangar, load

HERE = Path(__file__).parent


def test_the_skiff_as_it_arrived_has_its_top_inside_out():
    skiff = load(HERE.parent.parent / "bughunt" / "skiff.toml")
    assert inside_out(skiff) == [4]


def test_the_mended_skiff():
    assert inside_out(load(HERE / "skiff.toml")) == []


def test_every_ship_in_the_hangar():
    for ship in hangar():
        assert inside_out(ship) == [], ship.name
