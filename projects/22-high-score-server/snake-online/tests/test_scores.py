import json
from types import SimpleNamespace

import httpx
import pytest
from snake.model import State

from snake_online import scores
from snake_online.app import Reporter


class FakeServer:
    def __init__(self, working: bool = True) -> None:
        self.working = working
        self.received: list[dict] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        if not self.working:
            raise httpx.ConnectError("nobody home")
        body = json.loads(request.content)
        self.received.append(body)
        return httpx.Response(201, json={**body, "id": 1, "when": "now", "rank": 3})

    @property
    def client(self) -> httpx.Client:
        return httpx.Client(transport=httpx.MockTransport(self))


def test_a_score_is_posted_and_the_rank_comes_back(monkeypatch):
    monkeypatch.setattr(scores, "PLAYER", "ADA")
    server = FakeServer()
    row = scores.post_score("snake", 120, server.client)
    assert server.received == [{"game": "snake", "player": "ADA", "score": 120}]
    assert row is not None
    assert row["rank"] == 3


def test_a_server_that_is_away_is_a_warning_and_not_a_crash(caplog):
    assert scores.post_score("snake", 120, FakeServer(working=False).client) is None
    assert "The score wasn't recorded" in caplog.text


@pytest.mark.parametrize(
    ("number", "words"),
    [(1, "1st"), (2, "2nd"), (3, "3rd"), (4, "4th"), (11, "11th"), (12, "12th"),
     (13, "13th"), (21, "21st"), (102, "102nd"), (111, "111th")],
)  # fmt: skip
def test_ordinal(number, words):
    assert scores.ordinal(number) == words


def test_the_reporter_sends_each_game_once_at_the_moment_it_ends():
    server = FakeServer()
    reporter = Reporter(server.client)
    game = SimpleNamespace(state=State.PLAYING, score=70)
    for _ in range(3):
        reporter.watch(game)
    assert server.received == []

    game.state = State.GAME_OVER
    for _ in range(100):
        reporter.watch(game)
    assert len(server.received) == 1
    assert reporter.caption == "Snake: 70, and you came 3rd"

    game.state, game.score = State.PLAYING, 0
    reporter.watch(game)
    game.state, game.score = State.GAME_OVER, 20
    reporter.watch(game)
    assert [body["score"] for body in server.received] == [70, 20]
