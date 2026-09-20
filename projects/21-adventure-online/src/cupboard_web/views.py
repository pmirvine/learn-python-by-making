"""The addresses that the game answers to."""

import logging

from cupboard.engine import State, describe, respond
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from werkzeug.wrappers import Response

from cupboard_web.game import LONGEST_COMMAND, current_state, keep, token, token_matches

log = logging.getLogger(__name__)
bp = Blueprint("game", __name__)


def check_token() -> None:
    """Refuse a request that didn't come from a form of ours."""
    if not token_matches(request.form.get("token", "")):
        log.warning("A request with a bad token, from %s", request.remote_addr)
        abort(403)


@bp.get("/")
def play() -> str:
    state = current_state()
    return render_template(
        "game.html", state=state, scene=describe(state), token=token()
    )


@bp.post("/command")
def command() -> str | Response:
    check_token()
    text = request.form.get("text", "")[:LONGEST_COMMAND]
    state, reply = respond(current_state(), text)
    keep(state)

    if request.headers.get("HX-Request"):
        return render_template("_turn.html", text=text, reply=reply, state=state)
    flash(f"> {text}")
    flash(reply)
    return redirect(url_for("game.play"))


@bp.post("/restart")
def restart() -> Response:
    check_token()
    keep(State())
    return redirect(url_for("game.play"))
