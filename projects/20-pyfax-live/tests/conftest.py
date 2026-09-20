import json
from pathlib import Path

import httpx
import pytest
from flask import Flask
from flask.testing import FlaskClient

from pyfax_live import create_app

HERE = Path(__file__).parent
LONDON = json.loads((HERE / "london.json").read_text(encoding="utf-8"))


class FakeWeather:
    """Stands in for Open-Meteo. It counts the requests, and can be told to break."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self.working = True

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if not self.working:
            return httpx.Response(503, text="Service unavailable")
        return httpx.Response(200, json=LONDON)


@pytest.fixture
def weather() -> FakeWeather:
    return FakeWeather()


@pytest.fixture
def app(tmp_path: Path, weather: FakeWeather) -> Flask:
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "only for tests",
            "DATABASE": str(tmp_path / "test.sqlite3"),
            "CONTENT": str(HERE.parent / "content"),
            "HTTP_CLIENT": httpx.Client(transport=httpx.MockTransport(weather)),
        }
    )


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
