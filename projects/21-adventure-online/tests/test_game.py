from conftest import send, token_on
from flask import Flask
from flask.testing import FlaskClient

WALKTHROUGH = [
    "south", "e", "take the torch", "go south", "examine flowerpots", "take key",
    "n", "w", "unlock door with key", "w", "get cassette", "e", "up", "up",
    "load cassette",
]  # fmt: skip


def test_a_new_player_starts_in_the_cupboard(client: FlaskClient):
    page = client.get("/").text
    assert "Cupboard Under the Stairs" in page
    assert "Moves: 0" in page


def test_a_command_gets_a_piece_of_a_page_and_not_a_whole_one(client: FlaskClient):
    piece = send(client, "south")
    assert "<html" not in piece
    assert '<p class="typed">&gt; south</p>' in piece
    assert "Hall" in piece


def test_the_piece_also_carries_a_new_status_and_an_empty_prompt(client: FlaskClient):
    piece = send(client, "south")
    assert 'id="status" hx-swap-oob="true"' in piece
    assert "Moves: 1" in piece
    assert 'id="text"' in piece
    assert 'hx-swap-oob="true"' in piece.split('id="text"')[1]


def test_the_game_is_remembered_between_requests(client: FlaskClient):
    send(client, "south")
    send(client, "e")
    assert "torch" in send(client, "look")
    assert "Moves: 3" in client.get("/").text


def test_each_player_has_a_game_of_their_own(app: Flask):
    alice, bob = app.test_client(), app.test_client()
    send(alice, "south")
    assert "Moves: 1" in alice.get("/").text
    assert "Moves: 0" in bob.get("/").text
    assert "Cupboard Under the Stairs" in bob.get("/").text


def test_the_game_can_be_won_in_a_browser(client: FlaskClient):
    for text in WALKTHROUGH[:-1]:
        send(client, text)
    assert "You have won, in 15 moves." in send(client, WALKTHROUGH[-1])
    assert "You've won!" in client.get("/").text


def test_starting_again(client: FlaskClient):
    send(client, "south")
    response = client.post("/restart", data={"token": token_on(client)})
    assert response.status_code == 302
    assert "Moves: 0" in client.get("/").text


def test_it_works_with_no_javascript_at_all(client: FlaskClient):
    send(client, "south", htmx=False)
    page = client.get("/").text
    assert "<html" in page
    assert "&gt; south" in page
    assert "Hall" in page
    assert "Moves: 1" in page
