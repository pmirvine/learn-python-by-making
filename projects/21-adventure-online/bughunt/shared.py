"""A colleague's version of the game. "It works perfectly," they say. "I've played it."

    uv run flask --app bughunt/shared.py run

Play it in two different browsers at once, or in one ordinary window and one
private window, and take turns.
"""

from cupboard.engine import State, describe, respond
from flask import Flask, redirect, render_template_string, request, url_for
from werkzeug.wrappers import Response

PAGE = """
<!doctype html>
<title>The Colossal Cupboard</title>
<pre>{{ scene }}</pre>
<p>Moves: {{ moves }}</p>
<form method="post" action="{{ url_for('command') }}">
  &gt; <input name="text" autofocus> <button>Do it</button>
</form>
"""

app = Flask(__name__)
state = State()
last_reply = describe(state)


@app.get("/")
def play() -> str:
    return render_template_string(PAGE, scene=last_reply, moves=state.moves)


@app.post("/command")
def command() -> Response:
    global state, last_reply
    state, last_reply = respond(state, request.form.get("text", ""))
    return redirect(url_for("play"))
