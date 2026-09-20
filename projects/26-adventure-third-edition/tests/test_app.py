from pathlib import Path

from conftest import WALKTHROUGH, Parrot
from helpers import say, story
from textual.widgets import Input, RichLog

from adventure.app import AdventureApp, TheEnd
from adventure.colossal import Colossal
from adventure.widgets import MapPanel, StatusPanel


async def test_it_opens_with_the_first_room():
    app = AdventureApp(Colossal)
    async with app.run_test():
        assert app.title == "The Colossal Cupboard"
        assert "Coats press in on every side" in story(app)
        assert app.query_one(Input).has_focus


async def test_a_turn():
    app = AdventureApp(Colossal)
    async with app.run_test() as pilot:
        await say(pilot, "south")
        assert "> south" in story(app)
        assert "brown swirly carpet" in story(app)
        assert app.query_one(Input).value == ""
        assert app.query_one(StatusPanel).facts["Moves"] == "1"
        chart = app.query_one(MapPanel).chart
        assert chart is not None
        assert chart.here.label == "Hall"


async def test_long_replies_are_wrapped_to_fit():
    app = AdventureApp(Colossal)
    async with app.run_test(size=(80, 24)) as pilot:
        await say(pilot, "south")
        log = app.query_one(RichLog)
        assert max(len(line.text.rstrip()) for line in log.lines) <= log.size.width


async def test_f4_takes_a_move_back():
    app = AdventureApp(Colossal)
    async with app.run_test() as pilot:
        await say(pilot, "south")
        await pilot.press("f4")
        assert "Taken back." in story(app)
        assert app.query_one(StatusPanel).facts["Moves"] == "0"


async def test_saving_and_restoring_with_the_red_keys(tmp_path: Path):
    app = AdventureApp(Colossal, tmp_path / "save.json")
    async with app.run_test() as pilot:
        await say(pilot, "south")
        await pilot.press("f2")
        await say(pilot, "east")
        await pilot.press("f3")
        assert "Restored." in story(app)
        assert app.query_one(StatusPanel).facts["Moves"] == "1"


async def test_winning_and_playing_again():
    app = AdventureApp(Colossal)
    async with app.run_test() as pilot:
        for command in WALKTHROUGH:
            await say(pilot, command)
        assert isinstance(app.screen, TheEnd)
        await pilot.click("#again")
        assert not isinstance(app.screen, TheEnd)
        assert app.query_one(StatusPanel).facts["Moves"] == "0"
        assert "You have won" not in story(app)


async def test_any_game_of_the_right_shape_will_do():
    app = AdventureApp(Parrot)
    async with app.run_test() as pilot:
        await say(pilot, "hello")
        assert "Squawk! hello!" in story(app)
        assert not app.query(MapPanel)
        assert app.query_one(StatusPanel).facts == {"Heard": "1"}


async def test_a_game_that_cannot_take_moves_back_is_not_asked_to():
    app = AdventureApp(Parrot)
    async with app.run_test() as pilot:
        await say(pilot, "hello")
        await pilot.press("f4", "f2", "f3")
        assert "Taken back" not in story(app)
        assert app.check_action("undo", ()) is False
        assert app.check_action("help", ()) is True


async def test_quit_is_the_front_ends_word():
    app = AdventureApp(Parrot)
    async with app.run_test() as pilot:
        await say(pilot, "quit")
    assert app.return_code == 0
