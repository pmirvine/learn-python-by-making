"""The program: a window, the mouse, the keyboard, and files dropped from outside."""

from pathlib import Path

import pygame
from life import PATTERNS, Cell, parse, soup

from pixel_life import rle
from pixel_life.camera import Camera
from pixel_life.simulation import Simulation
from pixel_life.view import View

WINDOW_SIZE = (960, 720)
LEFT_BUTTON, RIGHT_BUTTON = 1, 3


def cells_between(start: Cell, end: Cell) -> list[Cell]:
    """Return the cells on a straight line from one cell to another, both included."""
    (x1, y1), (x2, y2) = start, end
    steps = max(abs(x2 - x1), abs(y2 - y1))
    if steps == 0:
        return [start]
    return [
        (round(x1 + (x2 - x1) * n / steps), round(y1 + (y2 - y1) * n / steps))
        for n in range(steps + 1)
    ]


class App:
    """Everything that the events can change: the universe, the view of it, and the brush."""

    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        self.simulation = Simulation()
        self.camera = Camera()
        self.view = View(window)
        self.message = "Draw with the mouse. Space runs, N steps, 1-9 are patterns."
        self.brush: bool | None = None  # True paints, False rubs out, None is up
        self.last_cell: Cell | None = None
        self.load_pattern(parse(PATTERNS["gun"]), "gun")

    def load_pattern(self, cells: set[Cell], name: str) -> None:
        self.simulation.load(cells)
        middle = (max(x for x, _ in cells) // 2, max(y for _, y in cells) // 2)
        self.camera.centre_on(middle, self.window.get_size())
        self.message = f"Loaded {name}: {len(cells):,} cells."

    def load_file(self, path: Path) -> None:
        try:
            cells = rle.parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, rle.RLEError) as error:
            self.message = f"Couldn't load {path.name}: {error}"
        else:
            self.load_pattern(cells, path.name)

    def paint_to(self, pixel: tuple[int, int]) -> None:
        """Paint, or rub out, from the last cell that was painted to the one under the pixel."""
        cell = self.camera.cell_at(pixel)
        for between in cells_between(self.last_cell or cell, cell):
            self.simulation.paint(between, alive=bool(self.brush))
        self.last_cell = cell

    def handle(self, event: pygame.event.Event) -> bool:
        """Deal with one event. Return False if it's time to stop."""
        match event.type:
            case pygame.QUIT:
                return False
            case pygame.KEYDOWN:
                return self.key(event.key)
            case pygame.MOUSEBUTTONDOWN if event.button == LEFT_BUTTON:
                # Start on a live cell and you rub out. Start on a dead one and you paint.
                self.brush = self.camera.cell_at(event.pos) not in self.simulation.live
                self.last_cell = None
                self.paint_to(event.pos)
            case pygame.MOUSEBUTTONUP if event.button == LEFT_BUTTON:
                self.brush = None
            case pygame.MOUSEMOTION if self.brush is not None:
                self.paint_to(event.pos)
            case pygame.MOUSEMOTION if event.buttons[RIGHT_BUTTON - 1]:
                self.camera.pan(*event.rel)
            case pygame.MOUSEWHEEL:
                factor = 1.25 if event.y > 0 else 0.8
                self.camera.zoom_about(pygame.mouse.get_pos(), factor)
            case pygame.DROPFILE:
                self.load_file(Path(event.file))
        return True

    def key(self, key: int) -> bool:
        simulation = self.simulation
        names = list(PATTERNS)
        match key:
            case pygame.K_ESCAPE:
                return False
            case pygame.K_SPACE:
                simulation.running = not simulation.running
            case pygame.K_n | pygame.K_RIGHT:
                simulation.step()
            case pygame.K_c:
                simulation.load(set())
            case pygame.K_r:
                left, top = self.camera.cell_at((0, 0))
                right, bottom = self.camera.cell_at(self.window.get_size())
                simulation.load(soup(right - left, bottom - top), at=(left, top))
            case pygame.K_EQUALS | pygame.K_PLUS:
                simulation.faster(2)
            case pygame.K_MINUS:
                simulation.faster(0.5)
            case _ if pygame.K_1 <= key <= pygame.K_9 and key - pygame.K_1 < len(names):
                name = names[key - pygame.K_1]
                self.load_pattern(parse(PATTERNS[name]), name)
        return True

    def frame(self, seconds: float) -> None:
        self.simulation.update(seconds)
        self.view.draw(self.simulation, self.camera, self.message)


def main() -> None:
    pygame.init()
    window = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("Life")
    clock = pygame.time.Clock()
    app = App(window)

    running = True
    while running:
        for event in pygame.event.get():
            running = app.handle(event) and running
        app.frame(clock.tick(60) / 1000)
        pygame.display.flip()

    pygame.quit()
