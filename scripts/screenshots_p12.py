"""Regenerate the Project 12 pictures, by letting an autopilot play Asteroids.

uv run --project projects/12-asteroids python scripts/screenshots_p12.py
"""

import math
import os
import random
from pathlib import Path

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
from asteroids.model import Controls, Game, State
from asteroids.view import View

ASSETS = Path(__file__).parent.parent / "docs" / "assets"


def autopilot(game: Game) -> Controls:
    """Turn towards the nearest rock, and keep firing. Thrust now and then."""
    ship = game.ship
    nearest = min(game.rocks, key=lambda rock: abs(rock.position - ship.position))
    dx, dy = nearest.position - ship.position
    wanted = math.degrees(math.atan2(dx, -dy)) % 360
    difference = (wanted - ship.heading + 180) % 360 - 180
    turn = 0 if abs(difference) < 4 else (1 if difference > 0 else -1)
    return Controls(
        turn=turn, thrust=abs(difference) < 20 and abs(ship.velocity) < 60, fire=True
    )


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    game = Game(random.Random(5))
    view = View(game, window)

    view.draw()
    pygame.image.save(window, ASSETS / "p12-title.png")

    game.start()
    for frame in range(60 * 14):
        if game.state is not State.PLAYING:
            break
        game.update(1 / 60, autopilot(game))
        if frame == 60 * 9:
            view.draw()
            pygame.image.save(window, ASSETS / "p12-asteroids.png")
            print(
                f"score {game.score}, {len(game.rocks)} rocks, {len(game.bullets)} bullets"
            )
    print(f"ended in {game.state.name}, score {game.score}, lives {game.lives}")


if __name__ == "__main__":
    main()
