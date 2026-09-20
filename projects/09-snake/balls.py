import random

import pygame

SIZE = 512
COLOURS = ["red", "green", "yellow", "blue", "magenta", "cyan"]


class Ball:
    def __init__(self):
        self.x = self.y = SIZE / 2
        self.dx, self.dy = random.uniform(-4, 4), random.uniform(-4, 4)
        self.radius = random.randint(6, 28)
        self.colour = random.choice(COLOURS)

    def move(self):
        self.x, self.y = self.x + self.dx, self.y + self.dy
        if not self.radius <= self.x <= SIZE - self.radius:
            self.dx = -self.dx
        if not self.radius <= self.y <= SIZE - self.radius:
            self.dy = -self.dy


pygame.init()
window = pygame.display.set_mode((SIZE, SIZE))
clock = pygame.time.Clock()
balls = [Ball() for _ in range(40)]

while not pygame.event.get(pygame.QUIT):
    window.fill("black")
    for ball in balls:
        ball.move()
        pygame.draw.circle(window, ball.colour, (ball.x, ball.y), ball.radius)
    pygame.display.flip()
    clock.tick(50)
