"""BASIC has two kinds of value, numbers and strings, and is strict about which is which."""

import math
import operator
from collections.abc import Callable

from tiny_basic.errors import BasicError

type Value = float | str

TRUE, FALSE = -1.0, 0.0  # as on the BBC Micro: every bit set, and none


def number(value: Value) -> float:
    """Insist on a number."""
    if isinstance(value, str):
        raise BasicError("Type mismatch")
    return value


def string(value: Value) -> str:
    """Insist on a string."""
    if not isinstance(value, str):
        raise BasicError("Type mismatch")
    return value


def show(value: Value) -> str:
    """Return a value as PRINT would show it: whole numbers have no decimal point."""
    if isinstance(value, str):
        return value
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))
    return f"{value:.9g}"


COMPARISONS: dict[str, Callable[[Value, Value], bool]] = {
    "=": operator.eq,
    "<>": operator.ne,
    "<": operator.lt,
    ">": operator.gt,
    "<=": operator.le,
    ">=": operator.ge,
}
ARITHMETIC: dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": lambda x, y: x / y,  # operator.truediv would do, but its hints are vague
    "^": math.pow,
    "DIV": lambda x, y: int(x / y),
    "MOD": lambda x, y: math.fmod(int(x), int(y)),
    "AND": lambda x, y: int(x) & int(y),
    "OR": lambda x, y: int(x) | int(y),
}


def combine(left: Value, sign: str, right: Value) -> Value:
    """Work out `left sign right`, for any of BASIC's operators."""
    if sign in COMPARISONS:
        if isinstance(left, str) != isinstance(right, str):
            raise BasicError("Type mismatch")
        return TRUE if COMPARISONS[sign](left, right) else FALSE
    if sign == "+" and isinstance(left, str) and isinstance(right, str):
        return left + right
    x, y = number(left), number(right)
    if y == 0 and sign in ("/", "DIV", "MOD"):
        raise BasicError("Division by zero")
    try:
        return float(ARITHMETIC[sign](x, y))
    except OverflowError:
        raise BasicError("Too big") from None
    except ValueError:
        raise BasicError("-ve root") from None
