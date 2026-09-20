"""A sprite editor, with tools, undo and redo."""

import argparse
from functools import partial
from pathlib import Path

import pygame

from sprite_editor.commands import Flip, History, Shift
from sprite_editor.sprite import Colour, Sprite, SpriteError
from sprite_editor.tools import Box, Bucket, Eraser, Line, Pencil, Picker, Tool
from sprite_editor.widgets import (
    PANEL,
    TEXT,
    Button,
    Canvas,
    Swatch,
    draw_actual_size,
)

SIZE = (640, 480)
COMMAND_KEYS = pygame.KMOD_CTRL | pygame.KMOD_META
COLOUR_KEYS: dict[str, Colour] = {".": None} | {str(n): n for n in range(8)}
ARROWS = {
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
}


class App:
    def __init__(self, window: pygame.Surface, sprite: Sprite, path: Path) -> None:
        self.window = window
        self.font = pygame.font.Font(None, 22)
        self.sprite = sprite
        self.path = path
        self.history = History(sprite)
        self.saved = list(self.history.done)
        self.canvas = Canvas(pygame.Rect(16, 16, 400, 400), sprite)
        self.colour: Colour = 7
        self.tools: list[Tool] = [
            Pencil(),
            Eraser(),
            Line(),
            Box(),
            Bucket(),
            Picker(on_pick=self.choose_colour),
        ]
        self.tool = self.tools[0]
        self.drawing = False
        self.message = ""
        self.buttons = self.make_buttons()

    def make_buttons(self) -> list[Button]:
        buttons: list[Button] = []
        colours: list[Colour] = [None, *range(8)]
        for number, colour in enumerate(colours):
            rect = pygame.Rect(440 + number % 3 * 60, 16 + number // 3 * 44, 56, 40)
            choose = partial(self.choose_colour, colour)
            chosen = partial(self.colour_is, colour)
            buttons.append(Swatch(rect, colour, choose, chosen))

        for number, tool in enumerate(self.tools):
            rect = pygame.Rect(440 + number % 2 * 90, 160 + number // 2 * 36, 86, 32)
            choose = partial(self.choose_tool, tool)
            chosen = partial(self.tool_is, tool)
            buttons.append(Button(rect, tool.name, choose, chosen))

        actions = {
            "Undo": self.history.undo,
            "Redo": self.history.redo,
            "Flip": partial(self.history.perform, Flip()),
            "Save": self.save,
        }
        for number, (label, action) in enumerate(actions.items()):
            rect = pygame.Rect(440 + number % 2 * 90, 280 + number // 2 * 36, 86, 32)
            buttons.append(Button(rect, label, action))
        return buttons

    def choose_colour(self, colour: Colour) -> None:
        self.colour = colour

    def colour_is(self, colour: Colour) -> bool:
        return self.colour == colour

    def choose_tool(self, tool: Tool) -> None:
        self.tool = tool

    def tool_is(self, tool: Tool) -> bool:
        return self.tool is tool

    @property
    def changed(self) -> bool:
        return self.history.done != self.saved

    def save(self) -> None:
        try:
            self.sprite.save(self.path)
        except OSError as error:
            self.message = f"Couldn't save: {error}"
        else:
            self.saved = list(self.history.done)
            self.message = f"Saved {self.path.name}"

    def handle(self, event: pygame.event.Event) -> bool:
        """Deal with one event. Return False when it's time to stop."""
        match event.type:
            case pygame.QUIT:
                return False
            case pygame.KEYDOWN:
                self.key(event.key, event.mod)
            case pygame.MOUSEBUTTONDOWN if event.button == 1:
                self.click(event.pos)
            case pygame.MOUSEMOTION if self.drawing:
                self.tool.drag(self.sprite, self.canvas.cell_at(event.pos))
            case pygame.MOUSEBUTTONUP if event.button == 1 and self.drawing:
                self.drawing = False
                if command := self.tool.release(self.sprite):
                    self.history.perform(command)
        return True

    def click(self, position: tuple[int, int]) -> None:
        self.message = ""
        for button in self.buttons:
            if button.rect.collidepoint(position):
                button.on_click()
                return
        if self.canvas.rect.collidepoint(position):
            self.drawing = True
            self.tool.press(self.sprite, self.canvas.cell_at(position), self.colour)

    def key(self, key: int, mod: int) -> None:
        letters = {tool.key: tool for tool in self.tools}
        name = pygame.key.name(key)
        if mod & COMMAND_KEYS:
            match name:
                case "z" if mod & pygame.KMOD_SHIFT:
                    self.history.redo()
                case "z":
                    self.history.undo()
                case "y":
                    self.history.redo()
                case "s":
                    self.save()
        elif name in letters:
            self.choose_tool(letters[name])
        elif name in COLOUR_KEYS:
            self.choose_colour(COLOUR_KEYS[name])
        elif name == "h":
            self.history.perform(Flip())
        elif key in ARROWS:
            self.history.perform(Shift(*ARROWS[key]))

    def draw(self) -> None:
        self.window.fill(PANEL)
        changes = self.tool.changes if self.drawing else {}
        self.canvas.draw(self.window, self.sprite, changes)
        for button in self.buttons:
            button.draw(self.window, self.font)

        left = 440
        for scale in (1, 2, 4):
            rect = draw_actual_size(self.window, self.sprite, (left, 368), scale)
            left = rect.right + 12

        star = "*" if self.changed else ""
        status = self.message or f"{self.tool.name}   {self.path.name}{star}"
        self.window.blit(self.font.render(status, True, TEXT), (16, 448))


def open_sprite(path: Path, size: int) -> Sprite:
    if not path.exists():
        return Sprite(size, size)
    try:
        return Sprite.load(path)
    except (OSError, SpriteError) as error:
        raise SystemExit(f"Can't open {path}: {error}") from error


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=Path("untitled.sprite"))
    parser.add_argument("--size", type=int, default=16, help="of a new sprite")
    args = parser.parse_args()

    sprite = open_sprite(args.path, args.size)
    pygame.init()
    window = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(f"Sprite editor: {args.path.name}")
    clock = pygame.time.Clock()
    app = App(window, sprite, args.path)

    running = True
    while running:
        for event in pygame.event.get():
            running = app.handle(event) and running
        app.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
