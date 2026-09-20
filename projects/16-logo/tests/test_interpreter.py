import pytest

from logo import Interpreter, LogoError
from logo.turtle import Recorder


@pytest.fixture
def said():
    return []


@pytest.fixture
def logo(said):
    return Interpreter(Recorder(), say=said.append)


def test_a_square(logo):
    logo.run("repeat 4 [fd 100 rt 90]")
    lines = logo.turtle.canvas.lines
    ends = [(round(x), round(y)) for _start, (x, y), _colour in lines]
    assert ends == [(0, 100), (100, 100), (100, 0), (0, 0)]
    assert logo.turtle.heading == 0


def test_the_pen_and_the_colours(logo):
    logo.run("setpc 1 fd 10 pu fd 10 pd setpc 4 bk 5")
    assert [colour for _start, _end, colour in logo.turtle.canvas.lines] == [1, 4]
    assert logo.turtle.y == 15


@pytest.mark.parametrize(
    ("sum", "answer"),
    [
        ("2 + 3 * 4", "14"),
        ("(2 + 3) * 4", "20"),
        ("10 - 4 - 3", "3"),
        ("2 * 3 + 4 * 5", "26"),
        ("7 / 2", "3.5"),
        ("-3 + 5", "2"),
        ("2 * -3", "-6"),
        ("10-3", "7"),
        ("10 - 3", "7"),
        ("-(2 + 3)", "-5"),
        ("1 + 1 = 2", "TRUE"),
        ("2 * 3 < 5", "FALSE"),
        ('"yes', "YES"),
        ("[a list of 4]", "A LIST OF 4"),
    ],
)
def test_arithmetic(logo, said, sum, answer):
    logo.run(f"print {sum}")
    assert said == [answer]


def test_a_minus_sign_after_a_space_belongs_to_the_number(logo, said):
    logo.run("setxy 30 -40")
    assert (logo.turtle.x, logo.turtle.y) == (30, -40)
    with pytest.raises(LogoError, match="You don't say what to do with -3"):
        logo.run("print 10 -3")
    assert said == ["10"]


def test_procedures_with_inputs(logo):
    logo.run("""
        to square :size
          repeat 4 [fd :size rt 90]
        end
        to window :size
          repeat 4 [square :size rt 90]
        end
        window 50
    """)
    assert len(logo.turtle.canvas.lines) == 16
    assert list(logo.procedures) == ["SQUARE", "WINDOW"]


def test_output_makes_a_procedure_into_a_function(logo, said):
    logo.run("""
        to factorial :n
          if :n < 2 [output 1]
          output :n * factorial :n - 1
        end
        print factorial 10
    """)
    assert said == ["3.6288e+06"]


def test_recursion_keeps_each_call_its_own_inputs(logo):
    logo.run("""
        to tree :size
          if :size < 10 [stop]
          fd :size
          lt 30 tree :size * 0.7
          rt 60 tree :size * 0.7
          lt 30 bk :size
        end
        tree 80
    """)
    assert len(logo.turtle.canvas.lines) == 126
    assert (round(logo.turtle.x, 6), round(logo.turtle.y, 6)) == (0, 0)


def test_variables_are_found_in_the_caller_and_make_changes_them_there(logo, said):
    logo.run("""
        to bump
          make "count :count + 1
        end
        to twice :count
          bump bump
          print :count
        end
        twice 5
        make "count 100
        bump
        print :count
    """)
    assert said == ["7", "101"]


def test_repcount_belongs_to_the_nearest_repeat(logo, said):
    logo.run("repeat 2 [repeat 2 [print repcount] print repcount * 10]")
    assert said == ["1", "2", "10", "1", "2", "20"]


def test_ifelse(logo, said):
    logo.run('repeat 3 [ifelse repcount = 2 [print "two] [print repcount]]')
    assert said == ["1", "TWO", "3"]


def test_random_is_in_range(logo, said):
    logo.run("repeat 50 [print random 6]")
    assert set(said) <= {"0", "1", "2", "3", "4", "5"}


def test_setxy_and_home_and_clearscreen(logo):
    logo.run("setxy 30 -40 rt 45 home")
    assert len(logo.turtle.canvas.lines) == 1
    assert (logo.turtle.x, logo.turtle.y, logo.turtle.heading) == (0, 0, 0)
    logo.run("cs")
    assert logo.turtle.canvas.lines == []


@pytest.mark.parametrize(
    ("program", "complaint"),
    [
        ("fd", "Not enough inputs to FD"),
        ("fd [1 2]", r"FORWARD doesn't like \[1 2\] as input"),
        ('setxy 1 "two', "SETXY doesn't like TWO as input"),
        ("setpc 8", "SETPENCOLOR doesn't like 8 as input"),
        ("jump 5", "I don't know how to JUMP"),
        ("3 + 4", "You don't say what to do with 7"),
        ("print fd 5", "PRINT needs a value, and didn't get one"),
        ("print :nope", "NOPE has no value"),
        ("print 1 + [2]", r"\+ doesn't like \[2\] as input"),
        ("print (1 + 2", r"a \( with no \)"),
        ("print 1 +", "something missing at the end"),
        ("print 1 / 0", "I can't divide by nought"),
        ("to fd end", "TO can't use FD as a name"),
        ("to 5 end", "TO can't use 5 as a name"),
        ("to x fd 5", "TO X has no END"),
        ("stop", "only make sense inside a TO"),
        ("repcount", "only makes sense inside a REPEAT"),
        ("repeat 3 fd 1", "REPEAT needs a value, and didn't get one"),
        ("repeat [fd 1] 3", "REPEAT needs a number"),
        ("if 5 [fd 1]", "IF needs something true or false"),
        ("to forever forever end forever", "too deep"),
    ],
)
def test_mistakes_are_reported_in_words(logo, program, complaint):
    with pytest.raises(LogoError, match=complaint):
        logo.run(program)


def test_a_mistake_inside_a_procedure_leaves_the_variables_tidy(logo):
    logo.run("to broken :size fd :size jump end")
    with pytest.raises(LogoError):
        logo.run("broken 10")
    assert len(logo.variables.maps) == 1
    assert logo.counts == []


def test_help_lists_each_command_once_with_its_example(logo, said):
    logo.run("help")
    assert "FORWARD 50   Move forward, drawing a line if the pen is down." in said
    assert len(said) == len(set(said))
    assert all(line[0].isupper() for line in said)
