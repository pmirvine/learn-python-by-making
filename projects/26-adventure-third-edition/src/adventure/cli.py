"""Where the two halves meet: the one module that chooses a game and a front end."""

from adventure.app import AdventureApp
from adventure.colossal import Colossal


def main() -> None:
    AdventureApp(Colossal).run()
