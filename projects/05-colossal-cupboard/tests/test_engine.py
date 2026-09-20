from cupboard.engine import State, describe, respond
from cupboard.world import ITEMS, PLAYER, ROOMS, START_PLACES

WALKTHROUGH = [
    "south",
    "e",
    "take the torch",
    "go south",
    "examine flowerpots",
    "take key",
    "n",
    "w",
    "unlock door with key",
    "w",
    "get cassette",
    "e",
    "up",
    "up",
    "load cassette",
]


def play(commands: list[str], state: State | None = None) -> tuple[State, str]:
    """Feed a list of commands to the game. Return the final state and last reply."""
    state = state or State()
    reply = ""
    for command in commands:
        state, reply = respond(state, command)
    return state, reply


def test_the_game_can_be_won():
    state, reply = play(WALKTHROUGH)
    assert state.won
    assert "You have won, in 15 moves." in reply


def test_a_new_game_starts_in_the_cupboard():
    assert "Cupboard Under the Stairs" in describe(State())


def test_walls_are_solid():
    state, reply = play(["north"])
    assert reply == "You can't go that way."
    assert state.location == "cupboard"


def test_the_study_is_locked_until_the_key_is_used():
    state, reply = play(["s", "w"])
    assert reply == "The study door is locked."
    assert state.location == "hall"

    state, reply = play(["unlock door"], state)
    assert reply == "You have nothing to unlock it with."


def test_the_key_is_hidden_until_the_flowerpots_are_examined():
    state, reply = play(["s", "e", "s", "take key"])
    assert reply == "I can't see any key here."

    state, reply = play(["x flowerpots"], state)
    assert "rusty key" in reply
    assert "key" in describe(state)


def test_taking_and_dropping():
    state, reply = play(["s", "e", "take torch"])
    assert reply == "Taken."
    assert state.places["torch"] == PLAYER
    assert "torch" not in describe(state)

    state, reply = play(["i"], state)
    assert reply == "You're carrying: torch."

    state, reply = play(["w", "drop torch", "look"], state)
    assert "You can see: torch." in reply


def test_some_things_are_too_big_to_carry():
    _, reply = play(["s", "e", "s", "take flowerpots"])
    assert reply == "You can't carry the flowerpots."


def test_the_attic_is_dark_without_the_torch():
    state, reply = play(["s", "u", "u"])
    assert state.location == "attic"
    assert "pitch dark" in reply


def test_the_cassette_only_loads_in_the_attic():
    _, reply = play([*WALKTHROUGH[:11], "load cassette"])
    assert reply == "There's nothing here to load it into."


def test_replies_to_things_that_do_not_work():
    expected = {
        "": "Pardon?",
        "   ": "Pardon?",
        "dance": "I don't know how to dance.",
        "sing a song": "I don't know how to sing.",
        "take unicorn": "I can't see any unicorn here.",
        "drop unicorn": "You aren't carrying any unicorn.",
        "i": "You're empty-handed.",
    }
    for typed, reply in expected.items():
        assert respond(State(), typed)[1] == reply, typed


def test_moves_are_counted_but_nonsense_is_free():
    state, _ = play(["look", "dance", "", "i"])
    assert state.moves == 2


def test_respond_never_changes_the_state_it_is_given():
    before = State()
    after, _ = play(["s", "e", "take torch"], before)
    assert before == State()
    assert after != before
    assert before.places is not after.places


def test_every_thing_has_a_description_and_every_exit_leads_somewhere():
    assert set(START_PLACES) == set(ITEMS)
    for room in ROOMS.values():
        for destination in room.exits.values():
            assert destination in ROOMS
