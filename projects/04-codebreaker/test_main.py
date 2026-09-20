import pytest

from main import COLOURS, HIT, MISS, NEAR, make_code, parse_guess, render_board, score


def test_codes_are_four_known_letters():
    for _ in range(100):
        code = make_code()
        assert len(code) == 4
        assert set(code) <= set(COLOURS)


def test_parse_guess_tidies_up():
    assert parse_guess("rgby") == "RGBY"
    assert parse_guess(" r g b y ") == "RGBY"


def test_parse_guess_wants_four_letters():
    with pytest.raises(ValueError, match="4 letters"):
        parse_guess("RGB")


def test_parse_guess_names_the_letters_it_doesnt_know():
    with pytest.raises(ValueError, match="P, X"):
        parse_guess("RXPX")


def test_all_hits():
    assert score("RGBY", "RGBY") == [HIT, HIT, HIT, HIT]


def test_all_misses():
    assert score("RRGG", "BBYY") == [MISS, MISS, MISS, MISS]


def test_right_colours_in_the_wrong_places():
    assert score("RGBY", "YBGR") == [NEAR, NEAR, NEAR, NEAR]


def test_a_mixture():
    assert score("RGBY", "RBMG") == [HIT, NEAR, MISS, NEAR]


def test_a_colour_is_only_near_as_often_as_it_is_spare():
    # There's one R in the code, and the first peg hits it. The other three
    # Rs in the guess have nothing left to be near to.
    assert score("RGBY", "RRRR") == [HIT, MISS, MISS, MISS]


def test_a_later_hit_beats_an_earlier_near():
    # The code's only G is hit by the last peg, so the first G is a miss.
    assert score("RRRG", "GBBG") == [MISS, MISS, MISS, HIT]


def test_two_spares_allow_two_nears():
    assert score("GGRR", "RRGG") == [NEAR, NEAR, NEAR, NEAR]
    assert score("GGRB", "RRGG") == [NEAR, MISS, NEAR, NEAR]


def test_score_leaves_its_arguments_alone():
    code, guess = "RGBY", "YYRR"
    score(code, guess)
    assert (code, guess) == ("RGBY", "YYRR")


def test_the_board_always_has_ten_rows():
    assert len(render_board([])) == 10
    history = [("RGBY", [HIT, MISS, MISS, NEAR])]
    rows = render_board(history)
    assert len(rows) == 10
    assert "[white on red] R [/]" in rows[0]
    assert rows[1] == rows[9]
