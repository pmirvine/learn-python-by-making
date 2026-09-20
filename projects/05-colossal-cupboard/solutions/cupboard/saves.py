"""Saving a game to a file, and getting it back."""

import json
from dataclasses import asdict
from pathlib import Path

from cupboard.engine import State


class SaveError(Exception):
    """A saved game couldn't be written, or couldn't be read."""


def save(state: State, path: Path) -> None:
    """Write the state of the game to a file, as JSON."""
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(asdict(state), file, indent=2)
    except OSError as error:
        raise SaveError(f"I couldn't save the game: {error}") from error


def load(path: Path) -> State:
    """Read the state of a game back from a file."""
    try:
        with path.open(encoding="utf-8") as file:
            return State(**json.load(file))
    except FileNotFoundError:
        raise SaveError("There's no saved game to restore.") from None
    except (OSError, ValueError, TypeError) as error:
        raise SaveError(f"I couldn't read the saved game: {error}") from error
