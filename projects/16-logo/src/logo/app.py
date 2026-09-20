"""Logo in a window: the picture above, and somewhere to type underneath."""

import argparse
import math
from pathlib import Path

import pygame

from logo import Interpreter, LogoError
from logo.tokens import tokenise
from logo.turtle import COLOURS, Point, SvgCanvas, Turtle

SIZE = (800, 600)
PICTURE_HEIGHT = 470
LINE_HEIGHT = 24
LINES_SHOWN = 4
PAPER = (0, 0, 0)
PANEL = (24, 24, 48)
WORDS = (255, 255, 255)
GREEN = (0, 255, 0)
WELCOME = "Welcome to Logo. Try HELP, or REPEAT 4 [FD 100 RT 90]"


class PygameCanvas:
    """A canvas that draws on a Pygame surface. It never mentions the Canvas protocol."""

    def __init__(self, size: tuple[int, int]) -> None:
        self.surface = pygame.Surface(size)
        self.clear()

    def to_screen(self, point: Point) -> tuple[int, int]:
        width, height = self.surface.get_size()
        return round(width / 2 + point[0]), round(height / 2 - point[1])

    def line(self, start: Point, end: Point, colour: int) -> None:
        pygame.draw.line(
            self.surface, COLOURS[colour], self.to_screen(start), self.to_screen(end)
        )

    def clear(self) -> None:
        self.surface.fill(PAPER)


def is_complete(text: str) -> bool:
    """Has every TO got its END, and every [ its ]? If not, there's more to come."""
    try:
        words = [token.text for token in tokenise(text) if token.kind != "quoted"]
    except LogoError:
        return True  # it's wrong, and not unfinished: let run() say why
    unclosed = words.count("[") - words.count("]")
    unended = words.count("TO") - words.count("END")
    return unclosed <= 0 and unended <= 0


class App:
    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        self.font = pygame.font.Font(None, 26)
        self.canvas = PygameCanvas((window.get_width(), PICTURE_HEIGHT))
        self.output: list[str] = [WELCOME]
        self.logo = Interpreter(self.canvas, say=self.output.append)
        self.typed = ""
        self.pending = ""  # the lines of a TO that hasn't reached its END yet
        self.history: list[str] = []
        self.recalled = 0

    def run(self, text: str) -> None:
        try:
            self.logo.run(text)
        except LogoError as error:
            self.output.append(str(error))

    def enter(self) -> None:
        """The user has pressed Return."""
        line, self.typed = self.typed, ""
        self.output.append(("> " if self.pending else "? ") + line)
        if line.strip():
            self.history.append(line)
        self.recalled = len(self.history)
        self.pending += line + "\n"
        if is_complete(self.pending):
            text, self.pending = self.pending, ""
            self.run(text)

    def recall(self, step: int) -> None:
        """Bring back an earlier line, with the up and down arrows."""
        self.recalled = max(0, min(len(self.history), self.recalled + step))
        older = self.recalled < len(self.history)
        self.typed = self.history[self.recalled] if older else ""

    def handle(self, event: pygame.event.Event) -> bool:
        """Deal with one event. Return False when it's time to stop."""
        match event.type:
            case pygame.QUIT:
                return False
            case pygame.TEXTINPUT:
                self.typed += event.text
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_RETURN | pygame.K_KP_ENTER:
                        self.enter()
                    case pygame.K_BACKSPACE:
                        self.typed = self.typed[:-1]
                    case pygame.K_UP:
                        self.recall(-1)
                    case pygame.K_DOWN:
                        self.recall(1)
                    case pygame.K_ESCAPE:
                        self.typed = self.pending = ""
        return True

    def draw(self) -> None:
        self.window.fill(PANEL)
        self.window.blit(self.canvas.surface, (0, 0))
        self.draw_turtle(self.logo.turtle)

        prompt = "> " if self.pending else "? "
        cursor = "_" if pygame.time.get_ticks() // 400 % 2 else " "
        lines = [*self.output[-LINES_SHOWN:], prompt + self.typed + cursor]
        for number, line in enumerate(lines):
            words = self.font.render(line, True, WORDS)
            self.window.blit(words, (12, PICTURE_HEIGHT + 8 + number * LINE_HEIGHT))

    def draw_turtle(self, turtle: Turtle) -> None:
        """Draw the turtle as a triangle, pointing the way that it's facing."""
        x, y = self.canvas.to_screen((turtle.x, turtle.y))
        corners = []
        for degrees, length in ((0, 14), (140, 10), (220, 10)):
            angle = math.radians(turtle.heading + degrees)
            corners.append((x + length * math.sin(angle), y - length * math.cos(angle)))
        pygame.draw.polygon(self.window, GREEN, corners, width=2)


def draw_to_svg(program: Path, picture: Path) -> None:
    """Run a Logo program with no window at all, and save what it drew."""
    canvas = SvgCanvas()
    logo = Interpreter(canvas)
    logo.run(program.read_text(encoding="utf-8"))
    canvas.save(picture)
    print(f"Saved {picture}, with {len(canvas.lines)} lines in it.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("program", nargs="?", type=Path, help="a file of Logo to run")
    parser.add_argument("--svg", type=Path, help="draw to this file, with no window")
    args = parser.parse_args()

    if args.svg:
        if not args.program:
            parser.error("--svg needs a program to run")
        try:
            draw_to_svg(args.program, args.svg)
        except (OSError, LogoError) as error:
            raise SystemExit(f"{args.program}: {error}") from error
        return

    pygame.init()
    window = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Logo")
    pygame.key.start_text_input()
    clock = pygame.time.Clock()
    app = App(window)
    if args.program:
        try:
            app.run(args.program.read_text(encoding="utf-8"))
        except OSError as error:
            app.output.append(f"{args.program}: {error}")

    running = True
    while running:
        for event in pygame.event.get():
            running = app.handle(event) and running
        app.draw()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
