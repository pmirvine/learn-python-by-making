"""Run a turtle program against the real turtle module, flat out, then close it.

    python tests/turtle_runner.py path/to/program.py

Needs a display. Animation is switched off and mainloop() returns at once, so
a program that would sit waiting for the window to be closed finishes instead.
Exits with a non-zero status if the program crashed or drew nothing.
"""

import runpy
import sys
import turtle
from pathlib import Path


def main() -> None:
    script = Path(sys.argv[1]).resolve()
    real_tracer = turtle.TurtleScreen.tracer

    turtle.TurtleScreen.tracer = lambda self, *_args, **_kwargs: real_tracer(self, 0)
    turtle.TurtleScreen.mainloop = lambda _self: None
    turtle._Screen.exitonclick = lambda _self: None
    turtle.mainloop = turtle.done = lambda: None

    # Python puts a script's own folder first on the import path; do the same.
    sys.path.insert(0, str(script.parent))
    runpy.run_path(str(script), run_name="__main__")

    screen = turtle.Screen()
    screen.update()
    items = len(screen.getcanvas().find_all())
    turtle.bye()
    if items < 2:
        raise SystemExit(f"{script.name} drew nothing")


if __name__ == "__main__":
    main()
