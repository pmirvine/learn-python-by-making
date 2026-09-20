import pytest

P01 = "01-hi-lo"


@pytest.mark.parametrize(
    ("reply", "expected"),
    [("10", "Too low."), ("90", "Too high."), ("42", "Got it!")],
)
def test_stage1_single_guess(play, reply, expected):
    out = play(f"{P01}/stages/stage1.py", [reply])
    assert expected in out
    assert "The number was 42." in out


def test_stage1_crashes_on_words_as_the_chapter_says(play):
    with pytest.raises(ValueError, match="invalid literal"):
        play(f"{P01}/stages/stage1.py", ["seven"])


def test_stage2_loops_and_counts(play):
    out = play(f"{P01}/stages/stage2.py", ["50", "25", "42"])
    assert out.count("Too high.") == 1
    assert out.count("Too low.") == 1
    assert "Got it in 3 guesses!" in out


def test_stage3_bad_input_costs_nothing(play):
    out = play(f"{P01}/stages/stage3.py", ["seven", "42"])
    assert "'seven' isn't a whole number." in out
    assert "Got it in 1 guess!" in out


def test_stage3_runs_out_of_guesses(play):
    out = play(f"{P01}/stages/stage3.py", ["1"] * 7)
    assert out.count("Too low.") == 7
    assert "Out of guesses. I was thinking of 42." in out


@pytest.mark.parametrize("script", ["main.py", "solutions/tweaks.py"])
def test_final_tracks_best_score_across_rounds(play, script):
    replies = ["50", "42", "y", "42", "yes please", "1", "42", "n"]
    out = play(f"{P01}/{script}", replies)
    assert "Got it in 2 guesses!" in out
    assert "That's a new best: 2." in out
    assert "That's a new best: 1." in out
    assert out.count("new best") == 2
    assert "Your best was 1." in out


def test_final_with_no_wins(play):
    out = play(f"{P01}/main.py", ["1"] * 7 + ["n"])
    assert out.rstrip().endswith("Thanks for playing.")


def test_tweaks_refuses_out_of_range_and_spots_near_misses(play):
    out = play(f"{P01}/solutions/tweaks.py", ["5000", "40", "500", "42", "n"])
    assert "Keep it between 1 and 1000." in out
    assert "Too low, but so close." in out
    assert "Too high." in out
    assert "Got it in 3 guesses!" in out


def test_extended_menu_and_statistics(play):
    # Normal allows 7 guesses and Easy allows 4; lose both rounds.
    replies = ["2"] + ["50"] * 7 + ["y", "1"] + ["9"] * 4 + ["n"]
    out = play(f"{P01}/solutions/extended.py", replies, secret=4)
    assert "between 1 and 100." in out
    assert "between 1 and 10." in out
    assert "You won 0 of 2 rounds." in out


def test_extended_average(play):
    replies = ["1", "5", "4", "y", "1", "4", "n"]
    out = play(f"{P01}/solutions/extended.py", replies, secret=4)
    assert "You won 2 of 2 rounds." in out
    assert "Average guesses per win: 1.5" in out


def test_reverse_finds_the_number(play):
    # Thinking of 37: 50 high, 25 low, 37 yes.
    out = play(f"{P01}/reverse.py", ["h", "l", "y"])
    assert "Is it 37?" in out
    assert "Got it in 3." in out


def test_reverse_notices_a_fib(play):
    out = play(f"{P01}/reverse.py", ["h"] * 7)
    assert "fib" in out
