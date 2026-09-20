import pytest

from tiny_basic import nodes
from tiny_basic.errors import BasicError
from tiny_basic.nodes import Binary, Number, Variable
from tiny_basic.parser import Parser, parse


def tree(text: str) -> nodes.Expression:
    return Parser(text).expression()


def test_multiplying_comes_before_adding():
    assert tree("2 + 3 * 4") == Binary(
        Number(2), "+", Binary(Number(3), "*", Number(4))
    )


def test_brackets_come_before_everything():
    assert tree("(2 + 3) * 4") == Binary(
        Binary(Number(2), "+", Number(3)), "*", Number(4)
    )


def test_taking_away_goes_from_left_to_right():
    assert tree("10 - 4 - 3") == Binary(
        Binary(Number(10), "-", Number(4)), "-", Number(3)
    )


def test_powers_go_from_right_to_left():
    assert tree("2 ^ 3 ^ 2") == Binary(
        Number(2), "^", Binary(Number(3), "^", Number(2))
    )


def test_a_minus_sign_holds_tighter_than_times_and_looser_than_a_power():
    assert tree("-A * 2") == Binary(nodes.Unary("-", Variable("A")), "*", Number(2))
    assert tree("-A ^ 2") == nodes.Unary("-", Binary(Variable("A"), "^", Number(2)))


def test_not_takes_in_a_whole_comparison():
    assert tree("NOT A = B") == nodes.Unary(
        "NOT", Binary(Variable("A"), "=", Variable("B"))
    )


def test_functions_with_and_without_brackets():
    assert tree('LEFT$("HELLO", 2)') == nodes.Call(
        "LEFT$", (nodes.String("HELLO"), Number(2))
    )
    assert tree("PI * 2") == Binary(nodes.Call("PI", ()), "*", Number(2))


def test_statements():
    assert parse('PRINT "X is "; X,') == (
        nodes.Print((nodes.String("X is "), ";", Variable("X"), ",")),
    )
    assert parse('LET X = 1 : Y$ = "two"') == (
        nodes.Let("X", Number(1)),
        nodes.Let("Y$", nodes.String("two")),
    )
    assert parse("FOR I = 10 TO 1 STEP -1") == (
        nodes.For("I", Number(10), Number(1), nodes.Unary("-", Number(1))),
    )
    assert parse("NEXT : NEXT I") == (nodes.Next(), nodes.Next("I"))
    assert parse('INPUT "Name? ", N$ : INPUT AGE') == (
        nodes.Input("Name? ", "N$"),
        nodes.Input("? ", "AGE"),
    )
    assert parse("CLS : REM tidy: up") == (
        nodes.Command("CLS", ()),
        nodes.Rem("tidy: up"),
    )


def test_if_takes_the_rest_of_the_line_and_a_bare_number_is_a_goto():
    assert parse("IF X THEN PRINT 1 : PRINT 2 ELSE 300") == (
        nodes.If(
            Variable("X"),
            (nodes.Print((Number(1),)), nodes.Print((Number(2),))),
            (nodes.Goto(300),),
        ),
    )


@pytest.mark.parametrize(
    ("line", "complaint"),
    [
        ("PRINT (1 + 2", r"Missing \)"),
        ("PRINT 1 +", "the line stops too soon"),
        ("PRINT 1 + * 2", r"I didn't expect \*"),
        ("X = 1 2", "I didn't expect 2"),
        ("IF X PRINT 1", "Missing THEN"),
        ("FOR I = 1", "Missing TO"),
        ("GOTO X", "there should be a line number here"),
        ("GOTO 1.5", "there should be a line number here"),
        ("LET 5 = X", "there should be a variable here"),
        ("FROB 12", "I don't know what to do with FROB"),
        ("PRINT 1 :", "there's a statement missing"),
        ('INPUT "Name" N$', "Missing ,"),
        ("THEN", "I don't know what to do with THEN"),
    ],
)
def test_mistakes_are_caught_when_the_line_is_typed(line, complaint):
    with pytest.raises(BasicError, match=complaint):
        parse(line)
