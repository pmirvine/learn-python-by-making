from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from high_scores import create_app


@pytest.fixture
def database(tmp_path: Path) -> Path:
    return tmp_path / "test.sqlite3"


@pytest.fixture
def client(database: Path) -> TestClient:
    return TestClient(create_app(database))


def play(client: TestClient, game: str, player: str, score: int) -> dict:
    response = client.post(
        "/scores", json={"game": game, "player": player, "score": score}
    )
    assert response.status_code == 201, response.text
    return response.json()
