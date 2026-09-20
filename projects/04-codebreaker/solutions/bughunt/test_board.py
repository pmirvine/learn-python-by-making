"""The failing tests that pin the board's bugs down. Try them on bughunt/boardgame.py."""

from boardgame import new_board, place, render


def test_a_guess_fills_one_row_only():
    board = new_board()
    place(board, 0, "RGBY")
    lines = render(board)
    assert lines[0] == "R G B Y"
    assert lines[1] == "· · · ·"


def test_every_game_starts_with_an_empty_board():
    first = new_board()
    place(first, 0, "RGBY")
    second = new_board()
    assert render(second)[0] == "· · · ·"
