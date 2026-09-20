"""Chopping one line of BASIC into tokens."""

import re
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Literal

from tiny_basic.errors import BasicError

type Kind = Literal["number", "string", "keyword", "name", "symbol"]

KEYWORDS = {
    "PRINT", "LET", "INPUT", "IF", "THEN", "ELSE", "GOTO", "GOSUB", "RETURN",
    "FOR", "TO", "STEP", "NEXT", "REPEAT", "UNTIL", "REM", "END",
    "AND", "OR", "NOT", "DIV", "MOD",
}  # fmt: skip

TOKEN = re.compile(
    r"""
      (?P<number>  \d+ (\.\d*)? | \.\d+  )
    | (?P<string>  "[^"]*"               )
    | (?P<word>    [A-Za-z][A-Za-z0-9_]* \$?  )   # COUNT, or NAME$
    | (?P<symbol>  <= | >= | <> | [-+*/^=<>(),;:]  )
    | (?P<space>   \s+                   )
    | (?P<mistake> .                     )
    """,
    re.VERBOSE,
)


@dataclass(frozen=True, slots=True)
class Token:
    kind: Kind
    text: str

    def __str__(self) -> str:
        return self.text


def tokenise(line: str) -> Iterator[Token]:
    """Yield the tokens of one line of BASIC."""
    for found in TOKEN.finditer(line):
        text = found.group()
        match found.lastgroup:
            case "space":
                pass
            case "number":
                yield Token("number", text)
            case "string":
                yield Token("string", text[1:-1])
            case "symbol":
                yield Token("symbol", text)
            case "word" if text.upper() == "REM":
                yield Token("keyword", "REM")
                yield Token("string", line[found.end() :].strip())
                return
            case "word" if text.upper() in KEYWORDS:
                yield Token("keyword", text.upper())
            case "word":
                yield Token("name", text.upper())
            case _ if text == '"':
                raise BasicError('Missing "')
            case _:
                raise BasicError(f"Mistake: I don't understand {text!r}")
