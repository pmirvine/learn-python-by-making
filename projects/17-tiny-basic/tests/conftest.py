import pytest

from tiny_basic import Machine


class Script:
    """A console for tests: it keeps what's written, and answers INPUT from a list."""

    def __init__(self, *replies: str) -> None:
        self.written: list[str] = []
        self.replies = list(replies)

    def write(self, text: str) -> None:
        self.written.append(text)

    def read(self, prompt: str) -> str:
        self.written.append(prompt)
        if not self.replies:
            raise EOFError
        return self.replies.pop(0)

    @property
    def text(self) -> str:
        return "".join(self.written)


@pytest.fixture
def console() -> Script:
    return Script()


@pytest.fixture
def machine(console: Script) -> Machine:
    return Machine(console)


def run(machine: Machine, program: str) -> str:
    """Type a program in, run it, and return everything that it printed."""
    for line in program.strip().splitlines():
        machine.enter(line.strip())
    machine.enter("RUN")
    console = machine.console
    assert isinstance(console, Script)
    return console.text
