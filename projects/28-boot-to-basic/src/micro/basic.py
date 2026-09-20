"""What this computer adds to Project 17's BASIC: graphics, sound, sprites and keys.

Nothing here touches the parser, or the machine. Every statement is a Python
function with a decorator on it, which puts it on the interpreter's lists.
"""

from collections.abc import Generator
from contextlib import contextmanager
from typing import TYPE_CHECKING

import beeb
import pygame
from pyfax import Colour
from tiny_basic.errors import BasicError
from tiny_basic.machine import Machine
from tiny_basic.registry import command, function
from tiny_basic.values import FALSE, TRUE, number, string

if TYPE_CHECKING:
    from micro.computer import Micro

# INKEY(-99) asks "is the space bar down?" These are the BBC's own numbers.
KEYS = {
    -1: pygame.K_LSHIFT, -2: pygame.K_LCTRL, -99: pygame.K_SPACE, -74: pygame.K_RETURN,
    -98: pygame.K_z, -67: pygame.K_x, -66: pygame.K_a, -82: pygame.K_s,
    -73: pygame.K_SEMICOLON, -105: pygame.K_SLASH,
    -26: pygame.K_LEFT, -122: pygame.K_RIGHT, -58: pygame.K_UP, -42: pygame.K_DOWN,
}  # fmt: skip


@contextmanager
def complaining() -> Generator[None]:
    """Turn Python's complaints into BASIC's, so that they stop the program, and not the computer."""
    try:
        yield
    except (ValueError, NotImplementedError) as error:
        raise BasicError(str(error)) from None


def whole(value: float | str) -> int:
    return int(number(value))


@command("MOVE")
def move(machine: Machine, x: float, y: float) -> None:
    beeb.move(number(x), number(y))


@command("DRAW")
def draw(machine: Machine, x: float, y: float) -> None:
    beeb.draw(number(x), number(y))


@command("PLOT")
def plot(machine: Machine, k: float, x: float, y: float) -> None:
    with complaining():
        beeb.plot(whole(k), number(x), number(y))


@command("GCOL")
def gcol(machine: Machine, action: float, colour: float) -> None:
    with complaining():
        beeb.gcol(whole(action), whole(colour))


@command("CLG")
def clg(machine: Machine) -> None:
    beeb.clg()


@command("SOUND")
def sound(
    machine: Machine, channel: float, amplitude: float, pitch: float, time: float
) -> None:
    with complaining():
        beeb.sound(whole(channel), whole(amplitude), whole(pitch), whole(time))


@command("ENVELOPE")
def envelope(
    machine: Machine, n: float, a: float, d: float, s: float, r: float
) -> None:
    with complaining():
        beeb.envelope(whole(n), number(a), number(d), number(s), number(r))


def install(micro: "Micro") -> None:
    """List the statements that have to know which computer they're running on.

    They're closures: each is made here, and remembers `micro`.
    """

    @command("MODE")
    def mode(machine: Machine, n: float) -> None:  # pyright: ignore[reportUnusedFunction]
        with complaining():
            micro.mode(whole(n))

    @command("CLS")
    def cls(machine: Machine) -> None:  # pyright: ignore[reportUnusedFunction]
        micro.screen.clear()

    @command("COLOUR")
    def colour(machine: Machine, n: float) -> None:  # pyright: ignore[reportUnusedFunction]
        micro.screen.ink = Colour(whole(n) % 8)

    @command("WAIT")
    def wait(machine: Machine) -> None:  # pyright: ignore[reportUnusedFunction]
        micro.waiting = True

    @command("SPRITE")
    def sprite(machine: Machine, n: float, name: str) -> None:  # pyright: ignore[reportUnusedFunction]
        with complaining():
            micro.sprites.define(
                whole(n), (micro.disc / string(name)).with_suffix(".sprite")
            )

    @command("PUT")
    def put(machine: Machine, n: float, x: float, y: float) -> None:  # pyright: ignore[reportUnusedFunction]
        with complaining():
            micro.sprites.put(whole(n), number(x), number(y))

    @command("HIDE")
    def hide(machine: Machine, n: float) -> None:  # pyright: ignore[reportUnusedFunction]
        with complaining():
            micro.sprites.hide(whole(n))

    @function("COLLIDE")
    def collide(a: float, b: float) -> float:  # pyright: ignore[reportUnusedFunction]
        with complaining():
            touching = micro.sprites.collide(whole(a), whole(b))
        return TRUE if touching else FALSE

    @function("EDGE")
    def edge(n: float) -> float:  # pyright: ignore[reportUnusedFunction]
        with complaining():
            return float(micro.sprites.edge(whole(n)))

    @function("TAB")
    def tab(column: float, row: float) -> str:  # pyright: ignore[reportUnusedFunction]
        """PRINT TAB(10, 5); "HELLO" works because this moves the cursor, and prints nothing."""
        micro.screen.move_to(whole(column), whole(row))
        return ""

    @function("INKEY")
    def inkey(n: float) -> float:  # pyright: ignore[reportUnusedFunction]
        """INKEY(-99): is the space bar down? INKEY(0): the next key that was typed, or -1."""
        if number(n) < 0:
            return TRUE if KEYS.get(whole(n)) in micro.held else FALSE
        while micro.typed:
            if character := micro.typed.popleft():
                return float(ord(character))
        return -1.0
