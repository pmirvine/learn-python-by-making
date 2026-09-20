import pytest

from pyfax.mosaic import ALL_DOTS, Dot, pack, stylesheet, unpack


def test_each_square_has_a_bit_of_its_own():
    assert [dot.value for dot in Dot] == [1, 2, 4, 8, 16, 32]
    assert Dot.TOP_LEFT | Dot.MIDDLE_LEFT | Dot.BOTTOM_LEFT == 0b010101
    assert sum(Dot) == ALL_DOTS == 63


def test_packing_a_picture():
    assert pack(["##", "#.", ".."]) == [[0b000111]]
    assert pack(["#.#.", "....", "....", ".#.#"]) == [[1, 1], [2, 2]]


def test_a_picture_need_not_be_a_tidy_size():
    assert pack(["#####"]) == [[3, 3, 1]]
    assert pack([]) == []
    assert pack(["#", "", "#"]) == [[0b010001]]


@pytest.mark.parametrize("dots", range(64))
def test_unpacking_is_packing_backwards(dots):
    assert pack(unpack(dots)) == [[dots]]


def test_unpack():
    assert unpack(0b100001) == ["#.", "..", ".#"]


def test_the_stylesheet_has_a_rule_for_every_character_that_is_not_empty():
    rules = stylesheet().splitlines()
    assert len(rules) == 63
    assert rules[0] == (
        ".m1 { background-image: linear-gradient(currentColor, currentColor); "
        "background-position: 0% 0%; }"
    )
    assert rules[-1].count("linear-gradient") == 6
    assert rules[-1].endswith("0% 0%, 100% 0%, 0% 50%, 100% 50%, 0% 100%, 100% 100%; }")
