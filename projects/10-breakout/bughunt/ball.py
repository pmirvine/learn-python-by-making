"""A ball that speeds up every time it bounces. It doesn't get as far as bouncing."""

import math

import pygame

SIZE = 512


class Ball:
    def __init__(self, speed: float) -> None:
        self.x = self.y = SIZE / 2
        self.angle = math.radians(35)
        self.speed = speed

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"A ball's speed must be more than zero, not {value}")
        self.speed = min(value, 900.0)

    def update(self, seconds: float) -> None:
        self.x += math.cos(self.angle) * self.speed * seconds
        self.y += math.sin(self.angle) * self.speed * seconds
        if not 0 <= self.x <= SIZE:
            self.angle = math.pi - self.angle
            self.speed *= 1.05
        if not 0 <= self.y <= SIZE:
            self.angle = -self.angle
            self.speed *= 1.05
        self.x = min(max(self.x, 0), SIZE)
        self.y = min(max(self.y, 0), SIZE)


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode((SIZE, SIZE))
    clock = pygame.time.Clock()
    ball = Ball(speed=200)

    while not pygame.event.get(pygame.QUIT):
        ball.update(clock.tick(60) / 1000)
        window.fill("black")
        pygame.draw.circle(window, "yellow", (ball.x, ball.y), 8)
        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
