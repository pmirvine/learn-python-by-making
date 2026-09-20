import sqlite3

import pytest
from flask import Flask
from flask.testing import FlaskClient
from test_site import text_of

from pyfax_live import db
from pyfax_live.letters import check


def test_nobody_has_written_yet(client: FlaskClient):
    assert "Nobody has written in yet." in text_of(client.get("/500.html").text)


def test_the_form_is_a_form(client: FlaskClient):
    form = client.get("/599.html").text
    assert '<form method="post">' in form
    assert "pyfax.js" not in form


def test_writing_in(client: FlaskClient):
    sent = client.post(
        "/599.html", data={"name": "Enid", "message": "More  hedgehogs,\nplease."}
    )
    assert sent.status_code == 302
    assert sent.headers["Location"] == "/500.html"

    page = text_of(client.get("/500.html").text)
    assert "Thank you. Your letter is below." in page
    assert "Enid writes:" in page
    assert "More hedgehogs, please." in page
    assert "Thank you" not in text_of(client.get("/500.html").text)


def test_the_newest_letter_comes_first(client: FlaskClient):
    for name in ("First", "Second", "Third"):
        client.post("/599.html", data={"name": name, "message": "Hello."})
    page = text_of(client.get("/500.html").text)
    assert page.index("Third writes:") < page.index("First writes:")


def test_awkward_customers(client: FlaskClient):
    message = "Robert'); DROP TABLE letters;-- <script>alert(1)</script>"
    client.post("/599.html", data={"name": "O'Brien & Sons", "message": message})
    html = client.get("/500.html").text
    assert "<script>alert" not in html
    assert "O'Brien & Sons writes:" in text_of(html)
    assert "DROP TABLE letters;--" in " ".join(text_of(html).split())


@pytest.mark.parametrize(
    ("name", "message", "complaint"),
    [
        ("", "Hello", "Please say who you are."),
        ("Enid", "   ", "Your letter is empty."),
        ("E" * 21, "Hello", "That name is too long"),
        ("Enid", "x" * 201, "Too long: 200 letters at most."),
        ("Enid", "Bell\x07", "be printed"),
    ],
)
def test_letters_that_will_not_do(client: FlaskClient, name, message, complaint):
    response = client.post("/599.html", data={"name": name, "message": message})
    assert response.status_code == 400
    assert complaint in response.text
    assert "Nobody has written in yet." in text_of(client.get("/500.html").text)


def test_what_was_typed_is_kept_when_the_form_comes_back(client: FlaskClient):
    response = client.post("/599.html", data={"name": "", "message": "Fish & chips"})
    assert "Fish &amp; chips</textarea>" in response.text


def test_check():
    assert check("Enid", "Hello") == []
    assert len(check("", "")) == 2


def test_the_database_layer_by_itself(app: Flask):
    with app.app_context():
        db.add_letter("Ada", "One")
        db.add_letter("Bob", "Two")
        assert [letter.name for letter in db.latest_letters(10)] == ["Bob", "Ada"]
        assert [letter.name for letter in db.latest_letters(1)] == ["Bob"]


def test_a_transaction_that_fails_leaves_nothing_behind(app: Flask):
    with app.app_context():
        connection = db.get_db()
        with pytest.raises(sqlite3.IntegrityError), connection:
            connection.execute(
                "INSERT INTO letters (name, message) VALUES ('Ada', 'One')"
            )
            connection.execute(
                "INSERT INTO letters (name, message) VALUES (NULL, 'Two')"
            )
        assert db.latest_letters(10) == []
