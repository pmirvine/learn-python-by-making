"""Repo-level checks for Project 3: its stage snapshots and its other programs.

The reader's own tests are in the project, in test_main.py.
"""

P03 = "03-dice-lab"


def test_stage1_rolls_twenty_times(play):
    out = play(f"{P03}/stages/stage1.py", [], secret=3)
    assert out.startswith("[6, 6, 6,")
    assert "Lowest 6, highest 6" in out
    assert "Average 6.00" in out
    assert "Sevens: 0" in out


def test_stage2_draws_a_bar_for_every_total(play):
    out = play(f"{P03}/stages/stage2.py", [], secret=4)
    lines = out.splitlines()
    assert lines[0] == "  2  0.0%"
    assert lines[6] == "  8 " + "█" * 50 + " 100.0%"
    assert "Most common: 8, which came up 1000 times." in out


def test_stage3_reports_on_ability_scores(play):
    out = play(f"{P03}/stages/stage3.py", [], secret=5)
    assert " 15 " + "█" * 50 + " 100.0%" in out
    assert "The first ten: [15, 15, 15, 15, 15, 15, 15, 15, 15, 15]" in out
    assert "Scores of 16 or more: 0 (0.0%)" in out
    assert "Longest streak: 2000 in a row, of 15" in out


def test_the_finished_lab(play):
    out = play(f"{P03}/main.py", ["9", "2", "lots", "0", "50"], secret=17)
    assert "Please choose from 1, 2, 3: 2" in out
    assert "'lots' isn't a whole number." in out
    assert "It needs to be more than zero." in out
    assert "Two twenty-sided dice, keeping the higher, 50 times:" in out
    assert "Average: 17.00" in out
    assert "Longest streak: 50 in a row, of 17" in out


def test_galton_board_prints_a_pile_and_a_scale(play):
    out = play(f"{P03}/galton.py", [])
    lines = out.splitlines()
    assert len(lines) == 17
    assert "█" in lines[-2]
    assert lines[-1].split() == [str(n) for n in range(13)]
