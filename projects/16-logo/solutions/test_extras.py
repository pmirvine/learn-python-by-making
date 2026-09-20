import logging

import extras
import pytest

from logo import Interpreter
from logo.registry import COMMANDS
from logo.turtle import Recorder


@pytest.fixture
def said():
    return []


@pytest.fixture
def logo(said):
    return Interpreter(Recorder(), say=said.append)


def test_the_new_commands_are_on_the_list_with_the_right_number_of_inputs():
    assert COMMANDS["SETH"] is COMMANDS["SETHEADING"]
    assert COMMANDS["SETHEADING"].inputs == 1
    assert COMMANDS["XCOR"].inputs == 0
    assert COMMANDS["SQRT"].function.__doc__ == extras.sqrt.__doc__


def test_they_work(logo, said):
    logo.run("fd 20 seth 90 fd 30 print xcor print ycor print sqrt 16")
    assert said == ["30", "20", "4"]


def test_three_decorators_deep_the_checks_still_happen(logo):
    with pytest.raises(Exception, match="SETHEADING doesn't like"):
        logo.run('seth "north')


def test_traced_commands_are_logged(logo, caplog):
    caplog.set_level(logging.DEBUG, logger="extras")
    logo.run("seth 45 print sqrt 9")
    assert caplog.messages == ["SETHEADING 45 -> None", "SQRT 9 -> 3.0"]
