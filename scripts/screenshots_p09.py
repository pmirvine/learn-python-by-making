"""Regenerate the Project 9 pictures, by letting an autopilot play Snake.

uv run --project projects/09-snake python scripts/screenshots_p09.py
"""

import os
import random
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from snake.model import Direction, Game, State
from snake.view import View

ASSETS = Path(__file__).parent.parent / "docs" / "assets"


def steer(game: Game) -> None:
    """Head for the food, by whichever way doesn't end in disaster at once."""
    hx, hy = game.snake.head()
    fx, fy = game.food

    def distance_after(direction: Direction) -> float:
        dx, dy = direction.value
        x, y = hx + dx, hy + dy
        blocked = (x, y) in game.snake.body
        outside = not (0 <= x < game.columns and 0 <= y < game.rows)
        if blocked or outside or direction is game.snake.heading.opposite():
            return float("inf")
        return abs(fx - x) + abs(fy - y)

    game.snake.turns.clear()
    game.turn(min(Direction, key=distance_after))


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode((768, 576))
    game = Game(rng=random.Random(9))
    view = View(game, window)

    view.draw()
    pygame.image.save(window, ASSETS / "p09-title.png")

    game.start()
    while game.state is State.PLAYING and game.score < 150:
        steer(game)
        game.step()
    view.draw()
    pygame.image.save(window, ASSETS / "p09-snake.png")
    print(f"Playing: score {game.score}, length {len(game.snake.body)}")

    while game.state is State.PLAYING:
        game.step()
    view.draw()
    pygame.image.save(window, ASSETS / "p09-game-over.png")
    print(f"Game over: best {game.best}")


if __name__ == "__main__":
    main()
