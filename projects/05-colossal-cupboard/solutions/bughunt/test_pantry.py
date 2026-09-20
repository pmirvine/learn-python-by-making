"""The failing tests that pin the pantry's bug down. Try them on bughunt/pantry.py."""

from pantry import ITEMS, PLAYER, START_PLACES, take


def test_everything_in_the_pantry_can_be_taken():
    for name in START_PLACES:
        places, reply = take(START_PLACES.copy(), "pantry", name)
        assert reply == "Taken.", name
        assert places[name] == PLAYER


def test_every_thing_that_has_a_place_has_a_description():
    assert set(START_PLACES) == set(ITEMS)


def test_things_that_are_not_there():
    _, reply = take(START_PLACES.copy(), "pantry", "unicorn")
    assert reply == "I can't see any unicorn here."
    _, reply = take(START_PLACES.copy(), "kitchen", "jam")
    assert reply == "I can't see any jam here."


def test_the_teapot_and_the_jam_are_too_much():
    places, _ = take(START_PLACES.copy(), "pantry", "teapot")
    _, reply = take(places, "pantry", "jam")
    assert reply == "You can't manage the jam as well."
