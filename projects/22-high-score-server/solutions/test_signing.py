from signing import is_genuine, signature

KEY = "a key that only the game and the server know"
SCORE = {"game": "snake", "player": "ADA", "score": 120}


def test_a_signed_score_is_accepted():
    assert is_genuine(SCORE, signature(SCORE, KEY), KEY)


def test_the_order_of_the_fields_does_not_matter():
    shuffled = {"score": 120, "player": "ADA", "game": "snake"}
    assert signature(shuffled, KEY) == signature(SCORE, KEY)


def test_a_score_that_has_been_improved_is_not():
    honest = signature(SCORE, KEY)
    assert not is_genuine(SCORE | {"score": 999_999}, honest, KEY)


def test_nor_is_one_signed_with_a_guess_at_the_key():
    assert not is_genuine(SCORE, signature(SCORE, "password"), KEY)
