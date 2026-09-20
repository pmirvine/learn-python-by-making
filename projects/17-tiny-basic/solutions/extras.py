"""Tweak 1: more functions and a command, in a file of their own.

Nothing in the parser or the machine had to change. Importing this is enough.
"""

import math
import time

from tiny_basic import Machine
from tiny_basic.registry import command, function
from tiny_basic.values import number, string


@function("TAN")
def tan(radians: float) -> float:
    return math.tan(number(radians))


@function("DEG")
def deg(radians: float) -> float:
    return math.degrees(number(radians))


@function("UPPER$")
def upper(text: str) -> str:
    return string(text).upper()


@function("INSTR")
def instr(text: str, wanted: str) -> float:
    """Where one string is inside another, counting from 1, or 0 if it isn't."""
    return float(string(text).find(string(wanted)) + 1)


@command("WAIT")
def wait(machine: Machine, hundredths: float) -> None:
    """WAIT 50 does nothing for half a second."""
    time.sleep(number(hundredths) / 100)
