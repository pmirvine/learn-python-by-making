from main import HIT, MISS, NEAR, hard_mode_problem, make_code, pegs, score


def test_codes_without_repeats():
    for _ in range(200):
        code = make_code(repeats=False)
        assert len(set(code)) == len(code)


def test_pegs_agree_with_score():
    for _ in range(500):
        code, guess = make_code(), make_code()
        marks = score(code, guess)
        assert pegs(code, guess) == (marks.count(HIT), marks.count(NEAR))


def test_pegs_with_repeated_colours():
    assert pegs("RGBY", "RRRR") == (1, 0)
    assert pegs("GGRR", "RRGG") == (0, 4)


def test_hard_mode_keeps_hits():
    history = [("RGBY", [HIT, MISS, MISS, MISS])]
    assert hard_mode_problem(history, "RMMM") is None
    assert hard_mode_problem(history, "MMMM") == "Peg 1 must be R."


def test_hard_mode_uses_nears():
    history = [("RGBY", [MISS, NEAR, MISS, MISS])]
    assert hard_mode_problem(history, "GMMM") is None
    assert hard_mode_problem(history, "MMMM") == "The guess must contain G."
