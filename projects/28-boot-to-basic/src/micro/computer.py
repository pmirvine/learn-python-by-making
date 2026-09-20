"""The computer: a screen, a keyboard, some sprites, a disc, and a BASIC to run them."""

import time
from collections import deque
from pathlib import Path

import beeb
import pygame
from pyfax import Colour
from tiny_basic import BasicError, Machine
from tiny_basic.nodes import Statement
from tiny_basic.parser import parse

from micro.basic import install
from micro.display import Display
from micro.editor import LineEditor
from micro.sprites import SpriteLayer
from micro.textscreen import TextScreen

FRAME_RATE = 50
THINKING_TIME = 0.012  # seconds of BASIC in each frame, which leaves some for drawing
BANNER = "\nPython Micro 64K\n\nTiny BASIC\n\n"
UNPRINTABLE = {pygame.K_RETURN: "\r", pygame.K_BACKSPACE: "\b"}


class Micro:
    """It's also BASIC's console: PRINT comes to write(), and INPUT to read()."""

    def __init__(self, disc: Path, frame_rate: int = FRAME_RATE) -> None:
        self.disc = disc
        self.frame_rate = frame_rate
        self.screen = TextScreen()
        self.editor = LineEditor(self.screen)
        self.machine = Machine(self)
        self.display = Display()
        self.clock = pygame.time.Clock()
        self.lines: deque[str] = deque()  # typed, with Return, and not yet dealt with
        self.typed: deque[str] = deque(maxlen=32)  # typed while a program runs
        self.held: set[int] = set()  # the keys that are down at this moment
        self.running = False
        self.reading = False  # an INPUT is waiting for a line
        self.waiting = False  # WAIT: no more BASIC until the next frame
        self.escaped = False
        self.frames = 0
        install(self)
        self.mode(1)
        self.write(BANNER + ">")

    # The console, as the interpreter sees it.

    def write(self, text: str) -> None:
        self.screen.write(text)

    def read(self, prompt: str) -> str:
        """Wait for a line, while the computer goes on around us. It's a loop within the loop."""
        self.write(prompt)
        self.reading = True
        try:
            while self.typed and not self.lines:  # whatever was typed ahead comes first
                self.edit(self.typed.popleft())
            while not self.lines:
                self.frame()
                if self.escaped:
                    raise KeyboardInterrupt
        finally:
            self.reading = False
        return self.lines.popleft()

    # The keyboard.

    def press(self, key: int, character: str = "") -> None:
        self.held.add(key)
        character = character or UNPRINTABLE.get(key, "")
        if key == pygame.K_ESCAPE:
            self.escaped = True
        elif self.running and not self.reading:
            self.typed.append(character)  # kept for INKEY(0), or for the next INPUT
        else:
            self.edit(character)

    def edit(self, character: str) -> None:
        """Give one character to the line editor."""
        if character in ("\r", "\n"):
            self.lines.append(self.editor.take())
        elif character in ("\b", "\x7f"):
            self.editor.rub_out()
        elif character:
            self.editor.type(character)

    def release(self, key: int) -> None:
        self.held.discard(key)

    def type_in(self, text: str) -> None:
        """Press the keys for some text. It's for tests, and for demonstrations."""
        for character in text:
            key = pygame.K_RETURN if character == "\n" else ord(character.lower())
            self.press(key, character)
            self.release(key)
            if character == "\n":
                self.frame()

    # Doing as it's told.

    def mode(self, number: int) -> None:
        """Change mode, which clears everything. MODE 7 is text alone, on a black screen."""
        beeb.mode(1 if number == 7 else number)
        pygame.display.set_caption("Python Micro")
        pygame.key.set_repeat(400, 40)
        self.sprites = SpriteLayer(beeb.canvas().get_size())
        self.screen.clear()
        self.screen.ink = Colour.WHITE

    def obey(self, line: str) -> None:
        """Deal with a line that's been typed at the prompt."""
        word, _, rest = line.strip().partition(" ")
        name = rest.strip(' "')
        try:
            match word.upper():
                case "RUN":
                    self.machine.variables.clear()
                    self.begin()
                case "SAVE" if name:
                    self.machine.save((self.disc / name).with_suffix(".bas"))
                case "LOAD" if name:
                    self.machine.load_file((self.disc / name).with_suffix(".bas"))
                case "CAT":
                    names = sorted(path.name for path in self.disc.iterdir())
                    self.write("\n".join(names) + "\n")
                case "" | "LIST" | "NEW":
                    self.machine.enter(line)
                case _ if word.isdecimal() or line.strip()[0].isdecimal():
                    self.machine.enter(line)
                case _:
                    self.begin(parse(line))
        except BasicError as error:
            self.write(f"\n{error}\n")
        if not self.running:
            self.write(">")

    def begin(self, immediate: tuple[Statement, ...] = ()) -> None:
        self.machine.load(immediate)
        self.running = True
        self.typed.clear()

    def think(self) -> None:
        """Run the program for a little while: until time's up, or WAIT, or the end."""
        self.waiting = False
        enough = time.perf_counter() + THINKING_TIME
        try:
            while not self.waiting and time.perf_counter() < enough:
                if self.escaped:
                    raise BasicError("Escape", self.line_number())
                if not self.machine.step():
                    self.finish()
                    return
        except BasicError as error:
            self.finish(f"{error}\n")

    def line_number(self) -> int | None:
        steps, pc = self.machine.steps, self.machine.pc
        return steps[pc][0] if pc < len(steps) else None

    def finish(self, message: str = "") -> None:
        self.machine.pc = len(self.machine.steps)
        self.running = self.escaped = False
        self.typed.clear()  # or a game's worth of Zs and Xs would arrive at the prompt
        if self.screen.column:
            self.write("\n")
        self.write(message + ">")

    # One fiftieth of a second.

    def frame(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                self.press(event.key, event.unicode)
            elif event.type == pygame.KEYUP:
                self.release(event.key)

        if self.running and not self.reading:
            self.think()
        elif not self.reading:
            self.escaped = False  # there's nothing to escape from
            while self.lines and not self.running:
                self.obey(self.lines.popleft())

        self.frames += 1
        cursor = (not self.running or self.reading) and self.frames % 32 < 16
        self.display.show(beeb.canvas(), self.sprites, self.screen, cursor)
        self.clock.tick(self.frame_rate)

    def run(self) -> None:
        beeb.sound(1, -12, 101, 3)
        while True:
            self.frame()
