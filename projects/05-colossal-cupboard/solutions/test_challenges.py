from cupboard.engine import State, describe, respond, score
from cupboard.saves import load, save


def play(commands, state=None):
    state = state or State()
    reply = ""
    for command in commands:
        state, reply = respond(state, command)
    return state, reply


def test_this_is_the_solutions_package():
    assert hasattr(State(), "visited")


def test_descriptions_list_the_exits():
    assert describe(State()).endswith("Exits: south.")
    _, reply = play(["s"])
    assert reply.endswith("Exits: north, east, west, up.")


def test_new_synonyms():
    _, reply = play(["walk south", "e", "grab torch", "inv"])
    assert reply == "You're carrying: torch."


def test_the_bathroom_and_its_duck():
    _, reply = play(["s", "u", "e", "take duck", "x duck"])
    assert reply == "A rubber duck. It has seen things."


def test_score_counts_rooms_once_each():
    state, _ = play(["s", "n", "s", "n", "s"])
    assert state.visited == ["cupboard", "hall"]
    assert score(state) == 10
    assert respond(state, "score")[1] == "You have 10 points, out of a possible 90."


def test_visited_rooms_survive_a_save(tmp_path):
    state, _ = play(["s", "e"])
    save(state, tmp_path / "game.json")
    assert load(tmp_path / "game.json") == state
