"""Chopping the text of a program into tokens."""

import re
from collections.abc import Iterator
from dataclasses import dataclass

from logo.errors import LogoError

NAME = r"[A-Za-z][A-Za-z0-9.?]*"
TOKEN = re.compile(
    rf"""
      (?P<comment>  ;[^\n]*          )   # from a semicolon to the end of the line
    | (?P<number>   (?: (?<![^\s\[(]) - )?     # a minus sign counts, after a space
                    \d+ (\.\d+)?     )   # 90 or 0.5 or -40
    | (?P<word>     {NAME}           )   # FORWARD
    | (?P<variable> :{NAME}          )   # :size, the value of a variable
    | (?P<quoted>   "{NAME}          )   # "size, the name of one
    | (?P<symbol>   [-+*/<>=()\[\]]  )
    | (?P<newline>  \n               )
    | (?P<space>    [ \t\r]+         )
    | (?P<mistake>  .                )   # anything else at all
    """,
    re.VERBOSE,
)


@dataclass(frozen=True, slots=True)
class Token:
    kind: str
    text: str
    line: int

    def __str__(self) -> str:
        return self.text


def tokenise(text: str) -> Iterator[Token]:
    """Yield the tokens of a program, one at a time, as they're asked for."""
    line = 1
    for found in TOKEN.finditer(text):
        kind = found.lastgroup or "mistake"
        match kind:
            case "newline":
                line += 1
            case "space" | "comment":
                pass
            case "mistake":
                raise LogoError(f"I don't understand {found.group()!r} on line {line}")
            case "word":
                yield Token("word", found.group().upper(), line)
            case "variable" | "quoted":
                yield Token(kind, found.group()[1:].upper(), line)
            case _:
                yield Token(kind, found.group(), line)
