"""Repo-level checks for Project 4: stages, the whole game, and the bug hunt.

The reader's own tests are in the project, in test_main.py.
"""

P04 = "04-codebreaker"


def test_stage1_checks_guesses_and_accepts_the_code(play):
    out = play(
        f"{P04}/stages/stage1.py", ["rgb", "rxpx", "gggg", "r g b y"], code="RGBY"
    )
    assert "(Psst. The code is RGBY.)" in out
    assert "A guess is 4 letters, such as RGBY." in out
    assert "I don't know P, X." in out
    assert "No." in out
    assert out.rstrip().endswith("Cracked it!")


def test_stage2_marks_each_peg(play):
    out = play(f"{P04}/stages/stage2.py", ["rbmg", "rgby"], code="RGBY")
    assert "hit  near miss near" in out
    assert "hit  hit  hit  hit" in out
    assert out.rstrip().endswith("Cracked it!")


def test_the_game_can_be_won(play):
    out = play(f"{P04}/main.py", ["rrgg", "rgb", "mgcb", "n"], code="MGCB")
    assert "A guess is 4 letters" in out
    assert "Guess 2 of 10" in out
    assert "Cracked it in 2!" in out


def test_the_game_can_be_lost_and_played_again(play):
    replies = ["rrrr"] * 10 + ["y"] + ["mgcb", "n"]
    out = play(f"{P04}/main.py", replies, code="MGCB")
    assert "Out of turns. The code was" in out
    assert "Cracked it in 1!" in out


def test_the_challenges_game_runs(play):
    replies = ["rgby", "mmmm", "mgcb", "n"]
    out = play(f"{P04}/solutions/main.py", replies, code="MGCB")
    assert "In the board game: 1 black, 1 white." in out
    assert "Hard mode: Peg 2 must be G." in out
    assert "Cracked it in 2!" in out


def test_the_scroller_scrolls(play):
    out = play(f"{P04}/scroller.py", [])
    lines = out.splitlines()
    assert len(lines) == 240
    assert "LEARN PYTHON BY" in lines[0]
    assert "EARN PYTHON BY M" in lines[1]


def test_the_bug_hunt_game_shows_the_symptom(play):
    out = play(f"{P04}/bughunt/boardgame.py", ["rrgg", "mgcb", "n"], code="MGCB")
    assert out.count("R R G G") == 10, "one guess should appear in all ten rows"


def test_the_fixed_board_game(play):
    out = play(
        f"{P04}/solutions/bughunt/boardgame.py", ["rrgg", "mgcb", "n"], code="MGCB"
    )
    assert out.count("R R G G") == 1
