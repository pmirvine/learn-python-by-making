import pytest

from cupboard.engine import State, respond
from cupboard.saves import SaveError, load, save


def test_a_saved_game_comes_back_the_same(tmp_path):
    state = State()
    for command in ["s", "e", "take torch"]:
        state, _ = respond(state, command)

    save(state, tmp_path / "game.json")

    assert load(tmp_path / "game.json") == state


def test_the_save_file_is_readable_json(tmp_path):
    save(State(), tmp_path / "game.json")
    text = (tmp_path / "game.json").read_text(encoding="utf-8")
    assert '"location": "cupboard"' in text


def test_restoring_when_nothing_was_saved(tmp_path):
    with pytest.raises(SaveError, match="no saved game"):
        load(tmp_path / "nothing.json")


def test_restoring_from_a_file_of_rubbish(tmp_path):
    rubbish = tmp_path / "game.json"
    rubbish.write_text("this is not JSON", encoding="utf-8")
    with pytest.raises(SaveError, match="couldn't read"):
        load(rubbish)


def test_restoring_from_the_wrong_sort_of_json(tmp_path):
    wrong = tmp_path / "game.json"
    wrong.write_text('{"lives": 3}', encoding="utf-8")
    with pytest.raises(SaveError, match="couldn't read"):
        load(wrong)


def test_saving_somewhere_impossible(tmp_path):
    with pytest.raises(SaveError, match="couldn't save"):
        save(State(), tmp_path / "no-such-folder" / "game.json")
