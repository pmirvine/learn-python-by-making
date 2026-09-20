"""Telling the high-score server how a game went. It's the same for any game."""

import getpass
import logging
import os
from typing import TypedDict

import httpx

log = logging.getLogger(__name__)

SERVER = os.environ.get("SCORES_SERVER", "http://127.0.0.1:8000")
PLAYER = os.environ.get("PLAYER", getpass.getuser())[:12].upper()


class ScoreRow(TypedDict):
    """The shape of what the server sends back. It's a dict, and this describes it."""

    id: int
    game: str
    player: str
    score: int
    when: str
    rank: int


def post_score(
    game: str, score: int, client: httpx.Client | None = None
) -> ScoreRow | None:
    """Send a score. If the server can't be reached, say so in the log, and carry on."""
    sender = client or httpx.Client()
    body = {"game": game, "player": PLAYER, "score": score}
    try:
        response = sender.post(f"{SERVER}/scores", json=body, timeout=2)
        response.raise_for_status()
    except httpx.HTTPError as error:
        log.warning("The score wasn't recorded: %s", error)
        return None
    return response.json()


def ordinal(number: int) -> str:
    """Return 1st, 2nd, 3rd, 4th, 11th, 21st and so on."""
    if number % 100 in (11, 12, 13):
        return f"{number}th"
    return f"{number}{ {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th') }"
