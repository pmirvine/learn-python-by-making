"""Each player's game, kept in their own session."""

import secrets
from dataclasses import asdict

from cupboard.engine import State
from flask import session

LONGEST_COMMAND = 80


def current_state() -> State:
    """Return this player's game, or a new one if they haven't one that makes sense."""
    try:
        return State(**session["state"])
    except (KeyError, TypeError):
        return State()


def keep(state: State) -> None:
    """Put the game back in the player's session."""
    session["state"] = asdict(state)


def token() -> str:
    """Return this player's secret token, making one if they haven't got one yet."""
    if "token" not in session:
        session["token"] = secrets.token_urlsafe()
    return session["token"]


def token_matches(offered: str) -> bool:
    """Did this request come from one of our own pages?"""
    return secrets.compare_digest(offered, token())
