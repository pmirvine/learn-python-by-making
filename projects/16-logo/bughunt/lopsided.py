"""A colleague's Logo, from before yours. Simple programs work. Trees come out wrong.

    uv run bughunt/lopsided.py

It draws examples/tree.logo into lopsided.svg. Open it in a browser.
"""

from pathlib import Path

from logo import Interpreter
from logo.interpreter import Procedure, Stop, Value
from logo.turtle import SvgCanvas

HERE = Path(__file__).parent


class ColleaguesLogo(Interpreter):
    """The same as yours, but for the way that it calls a procedure."""

    def invoke(self, procedure: Procedure, inputs: list[Value]) -> Value | None:
        self.variables.update(zip(procedure.parameters, inputs, strict=True))
        try:
            self.execute(procedure.body)
        except Stop as stop:
            return stop.value
        return None


def main() -> None:
    canvas = SvgCanvas()
    logo = ColleaguesLogo(canvas)
    logo.run((HERE.parent / "examples" / "tree.logo").read_text(encoding="utf-8"))
    canvas.save(Path("lopsided.svg"))
    turtle = logo.turtle
    print(f"Drew {len(canvas.lines)} lines, and saved lopsided.svg.")
    print("The turtle ought to be back where it started, at 0, -200.")
    print(f"It's at {turtle.x:.0f}, {turtle.y:.0f}.")


if __name__ == "__main__":
    main()
