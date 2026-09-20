"""The Colossal Cupboard, in a browser."""

import logging
import secrets
from collections.abc import Mapping

from flask import Flask, Response

from cupboard_web import views

log = logging.getLogger(__name__)

# What a page of ours is allowed to load: only things that come from our own site.
POLICY = "default-src 'self'; frame-ancestors 'none'"


def create_app(config: Mapping[str, object] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_HTTPONLY=True,
        MAX_CONTENT_LENGTH=4096,
    )
    app.config.from_prefixed_env("CUPBOARD")
    if config:
        app.config.from_mapping(config)
    if not app.config.get("SECRET_KEY"):
        log.warning(
            "No CUPBOARD_SECRET_KEY is set. Games will be lost at each restart."
        )
        app.config["SECRET_KEY"] = secrets.token_hex()

    @app.after_request
    def add_security_headers(response: Response) -> Response:
        response.headers["Content-Security-Policy"] = POLICY
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    app.register_blueprint(views.bp)
    return app
