"""The API: what programs can ask of the server, and what they get back."""

import asyncio
import sqlite3
from collections.abc import AsyncIterator, Iterator
from contextlib import closing
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Query, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from high_scores import store
from high_scores.models import GameName, GameSummary, NewScore, Score

STATIC = Path(__file__).parent / "static"
router = APIRouter()


def get_db(request: Request) -> Iterator[sqlite3.Connection]:
    """Open a connection for one request, and close it when the request is over."""
    with closing(store.connect(request.app.state.database)) as db:
        yield db


Db = Annotated[sqlite3.Connection, Depends(get_db)]
Limit = Annotated[int, Query(ge=1, le=100)]


@router.post("/scores", status_code=201)
def post_score(new: NewScore, db: Db) -> Score:
    """Record a score, and say where it came in the table."""
    return store.add(db, new)


@router.get("/scores/{game}")
def top_scores(game: GameName, db: Db, limit: Limit = 10) -> list[Score]:
    """The best scores for one game, highest first."""
    return store.top(db, game, limit)


@router.get("/games")
def list_games(db: Db) -> list[GameSummary]:
    """Every game that has a score, with how often it's been played."""
    return store.games(db)


async def changes(database: Path, game: str, pause: float = 1.0) -> AsyncIterator[str]:
    """Yield a message whenever there's a new score for a game. It never finishes."""
    seen = -1
    while True:
        with closing(store.connect(database)) as db:
            latest = store.newest(db, game)
        if latest != seen:
            seen = latest
            yield f"data: {latest}\n\n"
        await asyncio.sleep(pause)


@router.get("/scores/{game}/events")
async def score_events(game: GameName, request: Request) -> StreamingResponse:
    """A stream that says something whenever the table changes."""
    stream = changes(request.app.state.database, game)
    return StreamingResponse(stream, media_type="text/event-stream")


@router.get("/", include_in_schema=False)
async def board() -> FileResponse:
    return FileResponse(STATIC / "index.html")


def create_app(database: Path = Path("scores.sqlite3")) -> FastAPI:
    app = FastAPI(title="High scores", version="1.0.0")
    app.state.database = database
    with closing(store.connect(database)) as db:
        store.init(db)
    app.include_router(router)
    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    return app
