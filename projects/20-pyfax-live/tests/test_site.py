from html import unescape

from conftest import FakeWeather
from flask.testing import FlaskClient


def text_of(html: str) -> str:
    """Return what's written on a page, a row to a line."""
    rows = html.split('<div class="row">')[1:]
    lines = []
    for row in rows:
        cells = [piece.split("<")[0] for piece in row.split(">")[1::2]]
        lines.append(unescape("".join(cells[:40])).rstrip())
    return "\n".join(lines)


def test_the_front_door_leads_to_the_index(client: FlaskClient):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"] == "/100.html"
    index = client.get("/100.html")
    assert index.status_code == 200
    assert "Hedgehog wins village bake-off" in text_of(index.text)


def test_articles_are_pages_as_they_were(client: FlaskClient):
    page = client.get("/101.html")
    assert "fair's fair & it was a lovely sponge" in " ".join(
        text_of(page.text).split()
    )
    assert 'href="301.html"' in page.text


def test_a_page_that_is_not_there(client: FlaskClient):
    response = client.get("/777.html")
    assert response.status_code == 404
    assert "There's no such page." in text_of(response.text)
    assert client.get("/nonsense").status_code == 404


def test_the_stylesheet_and_the_script_are_served(client: FlaskClient):
    css = client.get("/style.css")
    assert css.mimetype == "text/css"
    assert ".m21 {" in css.text
    assert client.get("/pyfax.js").mimetype == "text/javascript"


def test_the_weather_is_live(client: FlaskClient, weather: FakeWeather):
    page = text_of(client.get("/301.html").text)
    assert "Weather for London" in page
    assert "Now: 14C, rain, wind 12 km/h" in page
    assert "Sunday       Monday       Tuesday" in page
    assert "Rain         Cloudy       Sunny" in page
    assert "16C / 10C    18C / 8C     22C / 11C" in page
    (request,) = weather.requests
    assert request.url.params["latitude"] == "51.5"


def test_the_forecast_is_only_fetched_now_and_then(
    client: FlaskClient, weather: FakeWeather
):
    for _ in range(5):
        client.get("/301.html")
    assert len(weather.requests) == 1


def test_when_the_weather_service_is_down_the_page_still_works(
    client: FlaskClient, weather: FakeWeather
):
    weather.working = False
    response = client.get("/301.html")
    assert response.status_code == 200
    assert "There's no forecast at the moment." in text_of(response.text)
