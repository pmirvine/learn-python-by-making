"""PyFax with a server: live weather, and letters from readers."""

import logging
import secrets
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path

import httpx
from flask import Flask
from jinja2 import ChoiceLoader, PackageLoader
from pyfax import Colour
from pyfax.build import classes
from pyfax.content import pages

from pyfax_live import db, letters, views, weather
from pyfax_live.cache import TimedCache
from pyfax_live.weather import Forecast, Place

log = logging.getLogger(__name__)

DEFAULTS = {
    "DATABASE": "pyfax.sqlite3",
    "CONTENT": "content",
    "PLACE": {"name": "London", "latitude": 51.5, "longitude": -0.12},
    "WEATHER_SECONDS": 600,
}


def create_app(config: Mapping[str, object] | None = None) -> Flask:
    """Make the application. Every test makes a new one, with settings of its own."""
    app = Flask(__name__)
    app.config.from_mapping(DEFAULTS)
    app.config.from_prefixed_env("PYFAX")
    if config:
        app.config.from_mapping(config)
    if not app.config.get("SECRET_KEY"):
        log.warning(
            "No PYFAX_SECRET_KEY is set. Making one up, until the next restart."
        )
        app.config["SECRET_KEY"] = secrets.token_hex()

    # Our own templates come first, and then the ones that belong to pyfax.
    loaders = [app.jinja_env.loader, PackageLoader("pyfax")]
    app.jinja_env.loader = ChoiceLoader([loader for loader in loaders if loader])
    app.jinja_env.filters["classes"] = classes

    today = datetime.now().astimezone().date()
    live = (weather.NUMBER, letters.NUMBER, letters.FORM)
    articles = pages(Path(app.config["CONTENT"]), today, others=live)
    index = articles[0]
    index.write(18, 1, "LIVE", Colour.MAGENTA)
    index.write(19, 1, "The weather, as it is now" + "." * 10, Colour.WHITE)
    index.write(19, 36, str(weather.NUMBER), Colour.CYAN, link=weather.NUMBER)
    index.write(20, 1, "Your letters" + "." * 23, Colour.WHITE)
    index.write(20, 36, str(letters.NUMBER), Colour.CYAN, link=letters.NUMBER)
    app.extensions["pyfax"] = views.Site(
        pages={page.number: page for page in articles},
        place=Place(**app.config["PLACE"]),
        forecasts=TimedCache[str, Forecast](app.config["WEATHER_SECONDS"]),
        client=app.config.get("HTTP_CLIENT") or httpx.Client(),
    )

    app.teardown_appcontext(db.close_db)
    with app.app_context():
        db.init_db()
    app.register_blueprint(views.bp)
    return app
