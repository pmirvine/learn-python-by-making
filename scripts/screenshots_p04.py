"""Regenerate the Project 4 picture: the end of a game of Codebreaker.

    uv run --project projects/04-codebreaker python scripts/screenshots_p04.py

Rich can record everything a Console prints and save it as an SVG, colours and
all. The board is drawn by the game's own functions, from a scripted game.
"""

import sys
from pathlib import Path

from rich.console import Console

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "projects" / "04-codebreaker"))

import main as codebreaker

CODE = "MGCB"
GUESSES = ["RRGG", "BBYY", "GBMC", "CGBM", "MGCB"]


def main() -> None:
    console = Console(
        record=True, width=40, force_terminal=True, color_system="truecolor"
    )
    history = [(guess, codebreaker.score(CODE, guess)) for guess in GUESSES]

    console.print("$ uv run main.py", highlight=False)
    console.print("[dim]...[/]")
    codebreaker.show_board(console, history)
    console.print(f"\n[bold green]Cracked it in {len(history)}![/]")

    picture = ROOT / "docs" / "assets" / "p04-codebreaker.svg"
    console.save_svg(str(picture), title="Codebreaker")
    print(f"-> {picture.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
