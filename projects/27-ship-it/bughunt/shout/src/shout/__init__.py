"""Says things, in a box."""

import sys

from rich.console import Console
from rich.panel import Panel


def boxed(words: list[str]) -> Panel:
    return Panel.fit(" ".join(words).upper() + "!", border_style="bold red")


def main() -> None:
    Console().print(boxed(sys.argv[1:] or ["hello"]))
