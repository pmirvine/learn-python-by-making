"""BASIC at a prompt, in the terminal, or running a program from a file."""

import argparse
import sys
import time
from collections.abc import Generator
from contextlib import contextmanager, nullcontext
from pathlib import Path

from tiny_basic.errors import BasicError
from tiny_basic.machine import Machine

BANNER = "Tiny BASIC\n"


class Terminal:
    """A console that's the terminal that Python is running in."""

    def write(self, text: str) -> None:
        print(text, end="", flush=True)

    def read(self, prompt: str) -> str:
        return input(prompt)


@contextmanager
def timed(label: str) -> Generator[None]:
    """Time whatever happens inside the `with`, and say how long it took."""
    started = time.perf_counter()
    try:
        yield
    finally:
        seconds = time.perf_counter() - started
        print(f"[{label}: {seconds:.3f} seconds]", file=sys.stderr)


def converse(machine: Machine) -> None:
    """Take lines from the keyboard until there are no more."""
    print(BANNER)
    while True:
        try:
            line = input(">")
        except EOFError:
            print()
            return
        if line.strip().upper() == "QUIT":
            return
        try:
            machine.enter(line)
        except BasicError as error:
            print(f"\n{error}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("program", nargs="?", type=Path, help="a .bas file to run")
    parser.add_argument("--time", action="store_true", help="say how long it took")
    args = parser.parse_args()

    machine = Machine(Terminal())
    if args.program is None:
        converse(machine)
        return

    try:
        with timed("loading") if args.time else nullcontext():
            machine.load_file(args.program)
        with timed("running") if args.time else nullcontext():
            machine.run()
    except BasicError as error:
        raise SystemExit(f"\n{error}") from None
