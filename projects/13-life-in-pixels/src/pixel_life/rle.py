"""Reading patterns in RLE, the format in which the Life community shares them.

A glider is `bob$2bo$3o!`. A `b` is a dead cell and an `o` a live one, a number
in front means "this many of the next thing", `$` ends a row, and `!` ends the
pattern. Lines that start with `#` are comments, and a line such as
`x = 3, y = 3, rule = B3/S23` gives the pattern's size.
"""

import re

from life import Cell

TOKEN = re.compile(r"(\d*)([bo$!])")


class RLEError(ValueError):
    """A pattern file that can't be understood."""


def parse(text: str) -> set[Cell]:
    """Turn the text of an RLE file into the set of its live cells."""
    lines = [line.strip() for line in text.splitlines()]
    body = "".join(line for line in lines if line and line[0] not in "#x")

    leftover = TOKEN.sub("", body).strip()
    if leftover:
        raise RLEError(f"I don't understand {leftover[:20]!r} in this pattern")

    live: set[Cell] = set()
    x = y = 0
    for count, tag in TOKEN.findall(body):
        times = int(count) if count else 1
        match tag:
            case "b":
                x += times
            case "o":
                live.update((x + n, y) for n in range(times))
                x += times
            case "$":
                x, y = 0, y + times
            case "!":
                return live
    raise RLEError("The pattern has no ! to end it")
