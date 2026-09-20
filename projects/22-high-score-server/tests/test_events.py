import asyncio
from contextlib import closing
from pathlib import Path

from high_scores import create_app, store
from high_scores.app import changes
from high_scores.models import NewScore


def test_the_stream_speaks_at_once_and_then_only_when_something_changes(database: Path):
    create_app(database)

    def post(score: int) -> None:
        with closing(store.connect(database)) as db:
            store.add(db, NewScore(game="snake", player="ADA", score=score))

    async def listen() -> list[str]:
        heard: list[str] = []
        stream = changes(database, "snake", pause=0.01)
        heard.append(await anext(stream))
        post(100)
        heard.append(await anext(stream))
        post(50)
        post(75)
        heard.append(await anext(stream))
        await stream.aclose()
        return heard

    assert asyncio.run(listen()) == ["data: 0\n\n", "data: 1\n\n", "data: 3\n\n"]


def test_many_listeners_cost_almost_nothing_while_they_wait(database: Path):
    create_app(database)

    async def listen_briefly() -> str:
        stream = changes(database, "snake", pause=0.2)
        first = await anext(stream)
        await stream.aclose()
        return first

    async def crowd() -> list[str]:
        return await asyncio.gather(*(listen_briefly() for _ in range(200)))

    assert asyncio.run(crowd()) == ["data: 0\n\n"] * 200
