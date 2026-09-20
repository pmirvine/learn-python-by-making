"""Regenerate the Project 10 pictures, by letting an autopilot play Breakout.

uv run --project projects/10-breakout python scripts/screenshots_p10.py
"""

import os
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from breakout.model import Game, State
from breakout.view import View

ASSETS = Path(__file__).parent.parent / "docs" / "assets"


def play(game: Game, seconds: float) -> None:
    """Play for a while, with the bat following the ball, a little off-centre."""
    for frame in range(int(seconds * 120)):
        if game.state is State.SERVE:
            game.serve()
        wobble = 14 if frame // 200 % 2 else -14
        target = game.ball.rect.centerx + wobble
        steer = (target > game.bat.rect.centerx + 3) - (
            target < game.bat.rect.centerx - 3
        )
        game.update(1 / 120, steer)


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode((960, 768))
    game = Game()
    view = View(game, window)

    view.draw()
    pygame.image.save(window, ASSETS / "p10-serve.png")

    play(game, 25)
    view.draw()
    pygame.image.save(window, ASSETS / "p10-breakout.png")
    print(f"Level {game.number + 1}: score {game.score}, {game.level!r}, {game.ball!r}")

    # Skip to the second level. (An autopilot can rally for ever without
    # reaching the last few bricks, as many a human player has too.)
    game.level.bricks.clear()
    play(game, 14)
    view.draw()
    pygame.image.save(window, ASSETS / "p10-invader.png")
    print(f"Level {game.number + 1}: score {game.score}, {game.level!r}")


if __name__ == "__main__":
    main()
