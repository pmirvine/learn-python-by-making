import pytest

from tiny_basic.errors import BasicError
from tiny_basic.peekable import Peekable
from tiny_basic.tokens import Token, tokenise


def texts(line: str) -> list[str]:
    return [str(token) for token in tokenise(line)]


def test_keywords_and_names_are_made_capital_and_strings_are_left_alone():
    assert list(tokenise('print "Hello"; name$')) == [
        Token("keyword", "PRINT"),
        Token("string", "Hello"),
        Token("symbol", ";"),
        Token("name", "NAME$"),
    ]


def test_two_character_symbols_come_out_whole():
    assert texts("IF A<=10 AND B<>C THEN") == [
        "IF", "A", "<=", "10", "AND", "B", "<>", "C", "THEN",
    ]  # fmt: skip


def test_numbers():
    assert texts("1 2.5 .5 3.") == ["1", "2.5", ".5", "3."]


def test_a_remark_swallows_the_rest_of_the_line():
    assert list(tokenise('REM anything: "goes')) == [
        Token("keyword", "REM"),
        Token("string", 'anything: "goes'),
    ]


@pytest.mark.parametrize(
    ("line", "complaint"),
    [
        ('PRINT "HELLO', 'Missing "'),
        ("PRINT 5 ? 3", r"Mistake: I don't understand '\?'"),
    ],
)
def test_mistakes(line, complaint):
    with pytest.raises(BasicError, match=complaint):
        list(tokenise(line))


def test_peeking_does_not_use_anything_up():
    letters = Peekable("abc")
    assert letters.peek() == "a"
    assert letters.peek() == "a"
    assert next(letters) == "a"
    assert list(letters) == ["b", "c"]
    assert letters.peek() is None
    with pytest.raises(StopIteration):
        next(letters)


def test_a_peekable_works_in_a_for_loop_with_any_iterable():
    numbers = Peekable(n * n for n in range(5))
    seen = []
    for number in numbers:
        seen.append((number, numbers.peek()))
    assert seen == [(0, 1), (1, 4), (4, 9), (9, 16), (16, None)]
