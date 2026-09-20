"""BASIC's built-in functions and simple commands. Importing this module lists them."""

import math
import random
import time
from typing import TYPE_CHECKING

from tiny_basic.errors import BasicError
from tiny_basic.registry import command, function
from tiny_basic.values import number, show, string

if TYPE_CHECKING:
    from tiny_basic.machine import Machine

STARTED = time.monotonic()


@function("RND")
def rnd(limit: float) -> float:
    """RND(6) is a whole number from 1 to 6. RND(1) is a fraction from 0 up to 1."""
    if number(limit) <= 1:
        return random.random()
    return float(random.randint(1, int(limit)))


@function("INT")
def int_(value: float) -> float:
    return float(math.floor(number(value)))


@function("ABS")
def abs_(value: float) -> float:
    return abs(number(value))


@function("SGN")
def sgn(value: float) -> float:
    return float((number(value) > 0) - (number(value) < 0))


@function("SQR")
def sqr(value: float) -> float:
    if number(value) < 0:
        raise BasicError("-ve root")
    return math.sqrt(value)


@function("SIN")
def sin(radians: float) -> float:
    return math.sin(number(radians))


@function("COS")
def cos(radians: float) -> float:
    return math.cos(number(radians))


@function("PI")
def pi() -> float:
    return math.pi


@function("TIME")
def time_() -> float:
    """Hundredths of a second since BASIC started, as on the BBC Micro."""
    return float(int((time.monotonic() - STARTED) * 100))


@function("LEN")
def len_(text: str) -> float:
    return float(len(string(text)))


@function("LEFT$")
def left(text: str, count: float) -> str:
    return string(text)[: int(number(count))]


@function("RIGHT$")
def right(text: str, count: float) -> str:
    wanted = int(number(count))
    return string(text)[-wanted:] if wanted > 0 else ""


@function("MID$")
def mid(text: str, start: float, count: float) -> str:
    first = max(int(number(start)) - 1, 0)
    return string(text)[first : first + int(number(count))]


@function("STRING$")
def string_(count: float, text: str) -> str:
    """STRING$(3, "ab") is "ababab"."""
    return string(text) * int(number(count))


@function("CHR$")
def chr_(code: float) -> str:
    return chr(int(number(code)))


@function("ASC")
def asc(text: str) -> float:
    return float(ord(string(text)[0])) if text else -1.0


@function("STR$")
def str_(value: float) -> str:
    return show(number(value))


@function("VAL")
def val(text: str) -> float:
    try:
        return float(string(text))
    except ValueError:
        return 0.0


@command("CLS")
def cls(machine: "Machine") -> None:
    machine.console.write("\x1b[2J\x1b[H")
