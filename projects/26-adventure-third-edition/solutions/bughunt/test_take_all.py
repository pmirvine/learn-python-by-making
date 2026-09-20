"""The bug hunt's failing test, and the mended function that passes it."""

from dataclasses import replace

from cupboard.engine import State, is_dark, things_at
from cupboard.world import ITEMS, PLAYER, START_PLACES


def take_all(state: State) -> tuple[State, str]:
    """Pick up everything in the room that can be carried."""
    if is_dark(state):
        return state, "You grope about in the dark, and find nothing."
    taken = [name for name in things_at(state, state.location) if ITEMS[name].portable]
    if not taken:
        return state, "There's nothing here to take."
    places = state.places | dict.fromkeys(taken, PLAYER)
    return replace(
        state, places=places, moves=state.moves + 1
    ), f"Taken: {', '.join(taken)}."


def test_the_state_that_went_in_is_not_changed():
    before = State(location="kitchen")
    after, reply = take_all(before)
    assert reply == "Taken: torch."
    assert after.places["torch"] == PLAYER
    assert before.places == START_PLACES
    assert before.places is not after.places


def test_nothing_to_take_is_not_a_move():
    before = State(location="hall")
    assert take_all(before) == (before, "There's nothing here to take.")
