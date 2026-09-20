import re

import pytest
from flask import Flask
from flask.testing import FlaskClient

from cupboard_web import create_app


@pytest.fixture
def app() -> Flask:
    return create_app({"TESTING": True, "SECRET_KEY": "only for tests"})


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def token_on(client: FlaskClient) -> str:
    """Fetch the game's page, as a browser would, and find the token in its form."""
    found = re.search(r'name="token" value="([^"]+)"', client.get("/").text)
    assert found is not None
    return found[1]


def send(client: FlaskClient, text: str, htmx: bool = True) -> str:
    """Type a command, as htmx would send it, and return what comes back."""
    headers = {"HX-Request": "true"} if htmx else {}
    data = {"text": text, "token": token_on(client)}
    response = client.post("/command", data=data, headers=headers)
    assert response.status_code == (200 if htmx else 302), response.text
    return response.text
