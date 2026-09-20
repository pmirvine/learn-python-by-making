import pytest
from conftest import play
from fastapi.testclient import TestClient


def test_posting_a_score_gets_it_back_with_a_rank(client: TestClient):
    first = play(client, "snake", "ADA", 120)
    assert first["rank"] == 1
    assert first["id"] == 1
    assert first["when"].startswith("20")
    assert play(client, "snake", "BOB", 300)["rank"] == 1
    assert play(client, "snake", "CAT", 200)["rank"] == 2


def test_the_table_is_in_order_and_has_the_ranks(client: TestClient):
    for player, score in [("ADA", 120), ("BOB", 300), ("CAT", 200), ("DOT", 300)]:
        play(client, "snake", player, score)
    table = client.get("/scores/snake").json()
    assert [(row["rank"], row["player"], row["score"]) for row in table] == [
        (1, "BOB", 300),
        (1, "DOT", 300),
        (3, "CAT", 200),
        (4, "ADA", 120),
    ]


def test_each_game_has_a_table_of_its_own(client: TestClient):
    play(client, "snake", "ADA", 120)
    play(client, "breakout", "ADA", 4000)
    assert [row["score"] for row in client.get("/scores/breakout").json()] == [4000]
    assert client.get("/scores/asteroids").json() == []
    assert client.get("/games").json() == [
        {"game": "breakout", "plays": 1, "best": 4000},
        {"game": "snake", "plays": 1, "best": 120},
    ]


def test_limit(client: TestClient):
    for score in range(15):
        play(client, "snake", "ADA", score)
    assert len(client.get("/scores/snake").json()) == 10
    assert len(client.get("/scores/snake", params={"limit": 3}).json()) == 3
    assert client.get("/scores/snake", params={"limit": 0}).status_code == 422
    assert client.get("/scores/snake", params={"limit": "lots"}).status_code == 422


@pytest.mark.parametrize(
    ("body", "where", "complaint"),
    [
        ({"game": "snake", "player": "ADA"}, "score", "Field required"),
        (
            {"game": "snake", "player": "ADA", "score": -1},
            "score",
            "greater than or equal",
        ),
        ({"game": "snake", "player": "ADA", "score": "lots"}, "score", "valid integer"),
        ({"game": "snake", "player": "ADA", "score": 9.5}, "score", "valid integer"),
        (
            {"game": "Snake!", "player": "ADA", "score": 1},
            "game",
            "should match pattern",
        ),
        (
            {"game": "snake", "player": "   ", "score": 1},
            "player",
            "at least 1 character",
        ),
        ({"game": "snake", "player": "A" * 13, "score": 1}, "player", "at most 12"),
    ],
)
def test_scores_that_will_not_do(client: TestClient, body, where, complaint):
    response = client.post("/scores", json=body)
    assert response.status_code == 422
    (problem,) = response.json()["detail"]
    assert problem["loc"] == ["body", where]
    assert complaint in problem["msg"]
    assert client.get("/scores/snake").json() == []


def test_what_arrives_is_tidied_and_converted(client: TestClient):
    kept = play(client, "snake", "  ADA  ", "250")  # type: ignore[arg-type]
    assert kept["player"] == "ADA"
    assert kept["score"] == 250


def test_a_game_with_a_silly_name_is_refused_in_the_address_too(client: TestClient):
    assert client.get("/scores/DROP TABLE").status_code == 422


def test_the_api_describes_itself(client: TestClient):
    schema = client.get("/openapi.json").json()
    assert schema["info"]["title"] == "High scores"
    assert set(schema["paths"]) == {
        "/scores",
        "/scores/{game}",
        "/games",
        "/scores/{game}/events",
    }
    new_score = schema["components"]["schemas"]["NewScore"]
    assert new_score["properties"]["score"]["maximum"] == 1_000_000_000
    assert client.get("/docs").status_code == 200


def test_the_board_and_its_files_are_served(client: TestClient):
    assert "<canvas" in client.get("/").text
    assert "EventSource" in client.get("/static/board.js").text
