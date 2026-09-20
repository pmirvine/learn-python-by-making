"""BASIC's built-in functions, and the simple commands, kept on two lists by decorators."""

import inspect
from collections.abc import Callable
from dataclasses import dataclass

from tiny_basic.values import Value


@dataclass(frozen=True, slots=True)
class Builtin:
    name: str
    function: Callable[..., Value | None]
    arguments: int


FUNCTIONS: dict[str, Builtin] = {}
COMMANDS: dict[str, Builtin] = {}


def function[F: Callable[..., Value]](name: str) -> Callable[[F], F]:
    """List a Python function as a BASIC function, such as INT or LEFT$."""

    def register(python: F) -> F:
        wanted = len(inspect.signature(python).parameters)
        FUNCTIONS[name] = Builtin(name, python, wanted)
        return python

    return register


def command[F: Callable[..., None]](name: str) -> Callable[[F], F]:
    """List a Python function as a BASIC command. Its first parameter is the machine."""

    def register(python: F) -> F:
        wanted = len(inspect.signature(python).parameters) - 1
        COMMANDS[name] = Builtin(name, python, wanted)
        return python

    return register
