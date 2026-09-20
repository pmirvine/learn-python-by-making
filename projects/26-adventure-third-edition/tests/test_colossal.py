from pathlib import Path

from conftest import WALKTHROUGH
from cupboard.world import ROOMS, START

from adventure.colossal import Colossal, layout
from adventure.game import Game, Mapped, Saveable, Undoable


def test_the_house_fits_on_a_grid():
    spots = layout(ROOMS, START)
    assert spots["cupboard"] == (0, 0, 0)
    assert spots["garden"] == (1, 2, 0)
    assert spots["attic"] == (0, 1, 2)
    assert len(set(spots.values())) == len(ROOMS)


def test_it_can_do_everything_that_the_front_end_might_ask():
    game: Game = Colossal()  # pyright checks this line, and pytest the next
    assert isinstance(game, Mapped)
    assert isinstance(game, Undoable)
    assert isinstance(game, Saveable)


def test_the_walkthrough_still_wins():
    game = Colossal()
    for command in WALKTHROUGH:
        reply = game.play(command)
    assert game.over
    assert "You have won, in 15 moves." in reply
    assert game.status() == {"Moves": "15", "Carrying": "torch, key, cassette"}


def test_a_move_can_be_taken_back():
    game = Colossal()
    game.play("south")
    game.play("east")
    assert "Hall" in game.undo()
    assert game.status()["Moves"] == "1"


def test_there_is_a_first_move():
    game = Colossal()
    game.undo()
    assert game.undo() == "There's nothing to take back."
    assert "Cupboard" in game.opening()


def test_nonsense_is_not_a_move():
    game = Colossal()
    game.play("xyzzy")
    assert len(game.history) == 1


def test_the_map_grows_as_you_explore():
    game = Colossal()
    assert [place.label for place in game.chart().places] == ["Cupboard"]
    game.play("south")
    chart = game.chart()
    assert {place.label for place in chart.places} == {"Cupboard", "Hall"}
    assert chart.here.label == "Hall"
    assert chart.here.exits == "newu"
    assert chart.caption == "Ground floor"


def test_taking_a_move_back_takes_it_off_the_map():
    game = Colossal()
    game.play("south")
    game.undo()
    assert [place.label for place in game.chart().places] == ["Cupboard"]


def test_a_dark_room_is_a_question_mark():
    game = Colossal()
    for command in ["s", "u", "u"]:
        game.play(command)
    chart = game.chart()
    assert chart.here.label == "?"
    assert chart.here.exits == ""
    assert chart.caption == "Second floor"


def test_saving_and_restoring(tmp_path: Path):
    game = Colossal()
    game.play("south")
    assert game.save(tmp_path / "save.json") == "Saved."
    later = Colossal()
    assert "The Hall" in later.restore(tmp_path / "save.json")
    assert later.state == game.state


def test_a_save_from_the_first_edition_will_do(tmp_path: Path):
    from cupboard.engine import State
    from cupboard.saves import save

    save(State(location="garden", moves=4), tmp_path / "save.json")
    game = Colossal()
    assert "The Garden" in game.restore(tmp_path / "save.json")


def test_nothing_to_restore(tmp_path: Path):
    assert (
        Colossal().restore(tmp_path / "none.json")
        == "There's no saved game to restore."
    )
