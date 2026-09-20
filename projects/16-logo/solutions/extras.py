"""Extend 1 and 2: more commands, in a file of their own, and a decorator that logs.

Nothing in the interpreter had to change. Importing this module is enough:

    import extras  # in app.py, or in a test
"""

import logging
import math
from collections.abc import Callable
from functools import wraps
from typing import Any

from logo.interpreter import Interpreter
from logo.registry import command, numeric, show

log = logging.getLogger(__name__)


def traced(function: Callable) -> Callable:
    """Log every call of a command, with its inputs, and whatever it handed back."""

    @wraps(function)
    def tracer(logo: Interpreter, *inputs: Any) -> Any:
        result = function(logo, *inputs)
        shown = " ".join(show(value) for value in inputs)
        log.debug("%s %s -> %s", function.__name__.upper(), shown, result)
        return result

    return tracer


@command("SETHEADING", "SETH")
@traced
@numeric
def setheading(logo: Interpreter, degrees: float) -> None:
    """SETHEADING 90   Face this way: 0 is up, and 90 is to the right."""
    logo.turtle.heading = degrees % 360


@command("XCOR")
def xcor(logo: Interpreter) -> float:
    """XCOR   How far to the right of the middle the turtle is."""
    return logo.turtle.x


@command("YCOR")
def ycor(logo: Interpreter) -> float:
    """YCOR   How far above the middle the turtle is."""
    return logo.turtle.y


@command("SQRT")
@traced
@numeric
def sqrt(logo: Interpreter, number: float) -> float:
    """SQRT 2   The square root."""
    return math.sqrt(number)
