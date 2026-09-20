"""Drawing the universe through the camera."""

import pygame

from pixel_life.camera import Camera
from pixel_life.simulation import Simulation

BACKGROUND = (8, 8, 24)
GRID = (28, 28, 56)
ALIVE = (120, 255, 140)
TEXT = (255, 255, 120)


class View:
    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        self.font = pygame.font.Font(None, 24)

    def draw(self, simulation: Simulation, camera: Camera, message: str = "") -> None:
        self.window.fill(BACKGROUND)
        width, height = self.window.get_size()
        left, top = camera.cell_at((0, 0))
        right, bottom = camera.cell_at((width, height))

        if camera.zoom >= 8:
            self.draw_grid(camera, left, top, right, bottom)

        size = max(1, round(camera.zoom) - (1 if camera.zoom >= 4 else 0))
        for cx, cy in simulation.live:
            if left <= cx <= right and top <= cy <= bottom:
                x, y = camera.pixel_of((cx, cy))
                self.window.fill(ALIVE, (x, y, size, size))

        state = "running" if simulation.running else "paused"
        status = (
            f"Generation {simulation.generation:,}   population {len(simulation.live):,}"
            f"   {simulation.speed:.0f} a second   {state}"
        )
        self.window.blit(self.font.render(status, True, TEXT), (12, 10))
        bottom_line = self.window.get_height() - 28
        self.window.blit(self.font.render(message, True, TEXT), (12, bottom_line))

    def draw_grid(
        self, camera: Camera, left: int, top: int, right: int, bottom: int
    ) -> None:
        width, height = self.window.get_size()
        for cx in range(left, right + 2):
            x, _ = camera.pixel_of((cx, 0))
            pygame.draw.line(self.window, GRID, (x - 1, 0), (x - 1, height))
        for cy in range(top, bottom + 2):
            _, y = camera.pixel_of((0, cy))
            pygame.draw.line(self.window, GRID, (0, y - 1), (width, y - 1))
