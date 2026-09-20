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
        size = max(1, round(camera.zoom) - (1 if camera.zoom >= 4 else 0))
        for cell in simulation.live:
            x, y = camera.pixel_of(cell)
            pygame.draw.rect(self.window, ALIVE, (x, y, size, size))

        state = "running" if simulation.running else "paused"
        status = (
            f"Generation {simulation.generation:,}   population {len(simulation.live):,}"
            f"   {simulation.speed:.0f} a second   {state}"
        )
        self.window.blit(self.font.render(status, True, TEXT), (12, 10))
        bottom_line = self.window.get_height() - 28
        self.window.blit(self.font.render(message, True, TEXT), (12, bottom_line))
