"""Extend 1: two snakes, one board. The point is how little had to change.

Snake was never told that there would only be one of it. Each instance has a
body, a heading and a queue of turns of its own, so a second player is a second
call of Snake(...), and a second dictionary of keys.
"""

import random

import pygame

from snake.model import Direction, Snake

CELL = 16
COLUMNS, ROWS = 48, 36

KEYS = [
    {
        pygame.K_UP: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
    },
    {
        pygame.K_w: Direction.UP,
        pygame.K_s: Direction.DOWN,
        pygame.K_a: Direction.LEFT,
        pygame.K_d: Direction.RIGHT,
    },
]
COLOURS = ["green", "cyan"]


def loser(snakes: list[Snake]) -> int | None:
    """Return the number of a snake that has just crashed, or None."""
    for number, snake in enumerate(snakes):
        x, y = snake.head()
        others = [cell for other in snakes if other is not snake for cell in other.body]
        outside = not (0 <= x < COLUMNS and 0 <= y < ROWS)
        if outside or snake.bites_itself() or snake.head() in others:
            return number
    return None


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode((COLUMNS * CELL, ROWS * CELL))
    clock = pygame.time.Clock()
    snakes = [Snake((12, 18)), Snake((36, 18), Direction.LEFT)]
    food = (24, 10)

    while loser(snakes) is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                for snake, keys in zip(snakes, KEYS, strict=True):
                    if event.key in keys:
                        snake.turn(keys[event.key])

        for snake in snakes:
            snake.advance()
            if snake.head() == food:
                snake.grow(3)
                food = (random.randrange(COLUMNS), random.randrange(ROWS))

        window.fill("black")
        pygame.draw.rect(
            window, "red", (food[0] * CELL, food[1] * CELL, CELL - 1, CELL - 1)
        )
        for snake, colour in zip(snakes, COLOURS, strict=True):
            for x, y in snake.body:
                pygame.draw.rect(
                    window, colour, (x * CELL, y * CELL, CELL - 1, CELL - 1)
                )
        pygame.display.flip()
        clock.tick(12)

    print(f"Player {2 - loser(snakes)} wins!")


if __name__ == "__main__":
    main()
    pygame.quit()
