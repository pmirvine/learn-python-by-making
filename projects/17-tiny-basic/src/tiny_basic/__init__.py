"""A small BASIC, in the manner of the BBC Micro's."""

from tiny_basic.errors import BasicError
from tiny_basic.machine import Console, Machine

__all__ = ["BasicError", "Console", "Machine"]
