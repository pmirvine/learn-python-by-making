import pytest

from logo.errors import LogoError
from logo.reader import Stream, read
from logo.tokens import Token, tokenise


def kinds_and_texts(text: str) -> list[tuple[str, str]]:
    return [(token.kind, token.text) for token in tokenise(text)]


def test_words_are_made_capital_and_numbers_are_left_alone():
    assert kinds_and_texts("fd 100 Rt 22.5") == [
        ("word", "FD"),
        ("number", "100"),
        ("word", "RT"),
        ("number", "22.5"),
    ]


def test_variables_and_names_lose_their_punctuation():
    assert kinds_and_texts('make "size :size+1') == [
        ("word", "MAKE"),
        ("quoted", "SIZE"),
        ("variable", "SIZE"),
        ("symbol", "+"),
        ("number", "1"),
    ]


def test_comments_and_space_vanish_and_lines_are_counted():
    tokens = list(tokenise("fd 1 ; go\n\n  rt 2"))
    assert [token.line for token in tokens] == [1, 1, 3, 3]


def test_it_is_lazy():
    tokens = tokenise("fd 100 £ rt 90")
    assert next(tokens) == Token("word", "FD", 1)
    assert next(tokens).text == "100"
    with pytest.raises(LogoError, match="I don't understand '£' on line 1"):
        next(tokens)


def test_brackets_become_lists_inside_lists():
    items = read(tokenise("repeat 2 [fd 1 repeat 3 [rt 2]] home"))
    assert [str(item) for item in items[:2]] == ["REPEAT", "2"]
    block = items[2]
    assert isinstance(block, list)
    assert [str(item) for item in block[:3]] == ["FD", "1", "REPEAT"]
    assert isinstance(block[4], list)
    assert str(items[3]) == "HOME"


@pytest.mark.parametrize(
    ("text", "complaint"),
    [("fd 1 ]", r"a \] on line 1 with no \["), ("repeat 4 [fd 1", r"a \[ with no \]")],
)
def test_brackets_have_to_match(text, complaint):
    with pytest.raises(LogoError, match=complaint):
        read(tokenise(text))


def test_a_stream_keeps_the_place():
    stream = Stream(read(tokenise("fd + 1")))
    assert stream.more
    assert str(stream.peek()) == "FD"
    assert str(stream.take()) == "FD"
    assert stream.next_is("+", "-")
    stream.take()
    stream.take()
    assert not stream.more
    assert stream.peek() is None
    assert not stream.next_is("+")
