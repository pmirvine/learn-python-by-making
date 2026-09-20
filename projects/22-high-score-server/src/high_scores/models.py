"""The shapes of the data that comes in, and the data that goes out."""

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

# A type, with a note attached to say what's allowed.
GameName = Annotated[str, StringConstraints(pattern=r"^[a-z0-9-]{1,20}$")]
PlayerName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=12)
]


class NewScore(BaseModel):
    """What a game sends when somebody has finished playing."""

    game: GameName
    player: PlayerName
    score: int = Field(ge=0, le=1_000_000_000)


class Score(NewScore):
    """A score that's been kept: it has a number, a time, and a place in the table."""

    id: int
    when: datetime
    rank: int


class GameSummary(BaseModel):
    game: GameName
    plays: int
    best: int
