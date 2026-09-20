"""The addresses that the site answers to, and what it does for each."""

import logging
from dataclasses import dataclass
from datetime import date, datetime
from importlib.resources import files

import httpx
from flask import (
    Blueprint,
    Response,
    abort,
    current_app,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from pyfax import Colour, Page
from pyfax.build import stylesheet
from werkzeug.wrappers import Response as Redirect

from pyfax_live import db, letters, weather
from pyfax_live.cache import TimedCache

log = logging.getLogger(__name__)
bp = Blueprint("pyfax", __name__)


@dataclass
class Site:
    """What the application keeps from one request to the next."""

    pages: dict[int, Page]
    place: weather.Place
    forecasts: TimedCache[str, weather.Forecast]
    client: httpx.Client


def site() -> Site:
    return current_app.extensions["pyfax"]


def today() -> date:
    return datetime.now().astimezone().date()


def forecast() -> weather.Forecast | None:
    """Return the forecast, which may be a few minutes old, or None if there isn't one."""
    here = site()
    try:
        return here.forecasts.get(
            here.place.name, lambda: weather.fetch(here.place, here.client)
        )
    except weather.WeatherError:
        log.exception("No forecast")
        return None


@bp.get("/")
def home() -> Redirect:
    return redirect(url_for("pyfax.show", number=100))


@bp.get("/<int:number>.html")
def show(number: int) -> str:
    if number == weather.NUMBER:
        page = weather.page(site().place, forecast(), today())
    elif number == letters.NUMBER:
        notice = " ".join(str(message) for message in get_flashed_messages())
        page = letters.page(db.latest_letters(10), today(), notice)
    elif number in site().pages:
        page = site().pages[number]
    else:
        abort(404)
    return render_template("page.html", page=page)


@bp.route(f"/{letters.FORM}.html", methods=["GET", "POST"])
def write() -> str | Redirect | tuple[str, int]:
    if request.method == "GET":
        return render_template("write.html", problems=[], name="", message="")

    name = request.form.get("name", "").strip()
    message = " ".join(request.form.get("message", "").split())
    problems = letters.check(name, message)
    if problems:
        form = render_template(
            "write.html", problems=problems, name=name, message=message
        )
        return form, 400
    db.add_letter(name, message)
    log.info("A letter from %s", name)
    flash("Thank you. Your letter is below.")
    return redirect(url_for("pyfax.show", number=letters.NUMBER))


@bp.get("/style.css")
def style() -> Response:
    return Response(stylesheet(), mimetype="text/css")


@bp.get("/pyfax.js")
def script() -> Response:
    text = (files("pyfax") / "static" / "pyfax.js").read_text(encoding="utf-8")
    return Response(text, mimetype="text/javascript")


@bp.app_errorhandler(404)
def not_found(error: Exception) -> tuple[str, int]:
    lost = Page(404, "No such page")
    lost.write(12, 8, "There's no such page.", Colour.YELLOW)
    lost.write(14, 8, "Try the index: 100", Colour.CYAN, link=100)
    return render_template("page.html", page=lost), 404
