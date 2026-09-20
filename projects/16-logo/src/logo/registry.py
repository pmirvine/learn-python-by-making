"""The list of Logo's built-in commands, and the decorators that put them on it."""

import inspect
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from logo.errors import LogoError


@dataclass(frozen=True)
class Primitive:
    name: str
    function: Callable[..., Any]
    inputs: int


COMMANDS: dict[str, Primitive] = {}


def command(*names: str) -> Callable:
    """Put a function on the list of commands, under one or more names."""

    def register(function: Callable) -> Callable:
        # Every command's first parameter is the interpreter. The rest are its inputs.
        inputs = len(inspect.signature(function).parameters) - 1
        primitive = Primitive(names[0], function, inputs)
        for name in names:
            COMMANDS[name] = primitive
        return function

    return register


def numeric(function: Callable) -> Callable:
    """Make a command refuse any input that isn't a number."""

    @wraps(function)
    def checked(logo: Any, *inputs: Any) -> Any:
        for value in inputs:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                name = function.__name__.rstrip("_").upper()
                raise LogoError(f"{name} doesn't like {show(value)} as input")
        return function(logo, *inputs)

    return checked


def show(value: object) -> str:
    """Return a value as Logo would print it."""
    match value:
        case bool():
            return str(value).upper()
        case float() | int():
            return f"{value:g}"
        case list():
            return "[" + " ".join(show(item) for item in value) + "]"
        case _:
            return str(value)
