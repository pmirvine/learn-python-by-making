from conftest import send, token_on
from flask.testing import FlaskClient


def test_what_the_player_types_is_escaped_when_it_is_shown_back(client: FlaskClient):
    piece = send(client, "<script>alert(1)</script>")
    assert "<script>" not in piece
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in piece


def test_a_post_with_no_token_is_refused(client: FlaskClient):
    client.get("/")
    assert client.post("/command", data={"text": "south"}).status_code == 403
    assert client.post("/restart").status_code == 403
    assert "Moves: 0" in client.get("/").text


def test_so_is_a_post_with_somebody_elses_token(app):
    mallory, victim = app.test_client(), app.test_client()
    stolen = token_on(mallory)
    victim.get("/")
    response = victim.post("/command", data={"text": "south", "token": stolen})
    assert response.status_code == 403


def test_a_get_never_changes_anything(client: FlaskClient):
    assert client.get("/command").status_code == 405
    assert client.get("/restart").status_code == 405


def test_the_cookie_is_signed_so_a_forged_one_is_ignored(client: FlaskClient):
    send(client, "south")
    client.set_cookie("session", "eyJzdGF0ZSI6eyJ3b24iOnRydWV9fQ.forged.signature")
    page = client.get("/").text
    assert "You've won!" not in page
    assert "Moves: 0" in page


def test_the_cookie_has_the_right_flags_and_pages_have_the_right_headers(client):
    response = client.get("/")
    cookie = response.headers["Set-Cookie"]
    assert "HttpOnly" in cookie
    assert "SameSite=Lax" in cookie
    assert response.headers["Content-Security-Policy"].startswith("default-src 'self'")
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_a_very_long_command_is_cut_short(client: FlaskClient):
    piece = send(client, "x" * 500)
    assert "x" * 80 in piece
    assert "x" * 81 not in piece
