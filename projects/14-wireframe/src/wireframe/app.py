"""The window, the keys, and the loop."""

from pathlib import Path

import pygame

from wireframe.matrix import rotation_x, rotation_y, rotation_z
from wireframe.model import Ship, hangar, load
from wireframe.view import Style, View

SIZE = (320, 240)
TURN = 90.0  # degrees a second, while a key is held down
DRIFT = (13.0, 29.0, 7.0)  # degrees a second about x, y and z, when left alone

type Turn = tuple[float, float, float]


def steering(pressed: pygame.key.ScancodeWrapper) -> Turn:
    """Read the keys that are being held down, as turns about x, y and z."""
    return (
        TURN * (int(pressed[pygame.K_DOWN]) - int(pressed[pygame.K_UP])),
        TURN * (int(pressed[pygame.K_RIGHT]) - int(pressed[pygame.K_LEFT])),
        TURN * (int(pressed[pygame.K_z]) - int(pressed[pygame.K_x])),
    )


class App:
    def __init__(self, window: pygame.Surface, ships: list[Ship]) -> None:
        self.view = View(window)
        self.ships = ships
        self.number = 0
        self.style = Style.WIRES
        self.drifting = True
        self.message = ""
        self.orientation = rotation_x(20) @ rotation_y(-30)
        self.distance = 3 * self.ship.radius

    @property
    def ship(self) -> Ship:
        return self.ships[self.number]

    def show(self, number: int) -> None:
        self.number = number % len(self.ships)
        self.distance = 3 * self.ship.radius
        self.message = ""

    def handle(self, event: pygame.event.Event) -> bool:
        """Deal with one event. Return False when it's time to stop."""
        match event.type:
            case pygame.QUIT:
                return False
            case pygame.KEYDOWN:
                self.key(event.key)
            case pygame.DROPFILE:
                self.load_file(Path(event.file))
        return True

    def key(self, key: int) -> None:
        match key:
            case pygame.K_TAB:
                self.show(self.number + 1)
            case pygame.K_h:
                styles = list(Style)
                self.style = styles[(styles.index(self.style) + 1) % len(styles)]
            case pygame.K_SPACE:
                self.drifting = not self.drifting
            case pygame.K_EQUALS | pygame.K_PLUS:
                self.distance = max(1.5 * self.ship.radius, self.distance / 1.1)
            case pygame.K_MINUS:
                self.distance = min(20 * self.ship.radius, self.distance * 1.1)

    def load_file(self, path: Path) -> None:
        try:
            ship = load(path)
            for face in ship.faces:
                pygame.Color(face.colour)  # a ValueError, if Pygame hasn't heard of it
        except (OSError, ValueError) as error:
            self.message = f"{path.name}: {error}"
        else:
            self.ships.append(ship)
            self.show(len(self.ships) - 1)

    def frame(self, seconds: float, turn: Turn) -> None:
        if self.drifting and not any(turn):
            turn = DRIFT
        x, y, z = (degrees * seconds for degrees in turn)
        step = rotation_x(x) @ rotation_y(y) @ rotation_z(z)
        self.orientation = step @ self.orientation
        self.view.draw(
            self.ship, self.orientation, self.distance, self.style, self.message
        )


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode(SIZE, pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Wireframe")
    clock = pygame.time.Clock()
    app = App(window, hangar())

    running = True
    while running:
        for event in pygame.event.get():
            running = app.handle(event) and running
        app.frame(clock.tick(60) / 1000, steering(pygame.key.get_pressed()))
        pygame.display.flip()

    pygame.quit()
