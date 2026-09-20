import math
from datetime import datetime

from flask import Flask, Response

app = Flask(__name__)


def hand(turn: float, length: float, width: float, colour: str = "white") -> str:
    """Return a line from the middle, where `turn` is 0 at twelve and 0.5 at six."""
    x = 100 + length * math.sin(turn * math.tau)
    y = 100 - length * math.cos(turn * math.tau)
    return (
        f'<line x1="100" y1="100" x2="{x:.1f}" y2="{y:.1f}" '
        f'stroke="{colour}" stroke-width="{width}" stroke-linecap="round"/>'
    )


@app.get("/")
def clock() -> Response:
    now = datetime.now().astimezone()
    minutes = now.minute + now.second / 60
    hands = hand((now.hour % 12 + minutes / 60) / 12, 50, 6) + hand(minutes / 60, 75, 4)
    hands += hand(now.second / 60, 85, 1, "red")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">'
        f'<circle cx="100" cy="100" r="95" fill="navy" stroke="gold"/>{hands}</svg>'
    )
    return Response(svg, mimetype="image/svg+xml", headers={"Refresh": "1"})
