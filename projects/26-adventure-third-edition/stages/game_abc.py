"""The road not taken: the same bargain, as an abstract base class."""

from abc import ABC, abstractmethod


class Game(ABC):
    """Something that can be played by typing at it. Inherit from this."""

    title = "An adventure"

    @property
    @abstractmethod
    def over(self) -> bool: ...

    @abstractmethod
    def opening(self) -> str: ...

    @abstractmethod
    def play(self, text: str) -> str: ...

    def status(self) -> dict[str, str]:
        """Return a few facts worth keeping in view. There are none, unless you say so."""
        return {}

    def play_all(self, commands: list[str]) -> list[str]:
        """Play several turns. Every game gets this one free."""
        return [self.play(command) for command in commands]
