"""A full-screen front end for a text adventure. Which adventure, it doesn't know."""

from collections.abc import Callable
from pathlib import Path
from typing import ClassVar

from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Input, Label, RichLog

from adventure.game import Game, Mapped, Saveable, Undoable
from adventure.widgets import MapPanel, StatusPanel

HELP = "The red keys: F1 help, F2 save, F3 restore, F4 take a move back. Ctrl+Q quits."


class TheEnd(ModalScreen[bool]):
    """Shown over the game when it's over. It answers: again?"""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.heading = title

    def compose(self) -> ComposeResult:
        with Vertical(id="ending"):
            yield Label(f"{self.heading}\n\nThe end.")
            with Horizontal(id="buttons"):
                yield Button("Play again", variant="success", id="again")
                yield Button("Quit", id="quit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "again")


class AdventureApp(App[None]):
    CSS_PATH = Path(__file__).with_name("adventure.tcss")
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("f1", "help", "Help"),
        Binding("f2", "save", "Save"),
        Binding("f3", "restore", "Restore"),
        Binding("f4", "undo", "Take back"),
    ]

    def __init__(
        self, new_game: Callable[[], Game], save_file: Path = Path("cupboard-save.json")
    ) -> None:
        super().__init__()
        self.new_game = new_game
        self.game = new_game()
        self.save_file = save_file

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="story"):
                yield RichLog(id="transcript", wrap=True, min_width=20)
                yield Input(id="prompt", placeholder="What now?")
            with Vertical(id="side"):
                if isinstance(self.game, Mapped):
                    yield MapPanel()
                yield StatusPanel()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(StatusPanel).border_title = "Status"
        self.begin()

    def begin(self) -> None:
        self.title = self.game.title
        self.query_one(RichLog).clear()
        self.say(self.game.opening())
        self.query_one(Input).focus()

    def say(self, reply: str) -> None:
        """Add a reply to the story, and bring the panels up to date."""
        self.query_one(RichLog).write(Text(reply + "\n"))
        self.query_one(StatusPanel).facts = self.game.status()
        if isinstance(self.game, Mapped):
            self.query_one(MapPanel).chart = self.game.chart()

    @on(Input.Submitted)
    def take_a_turn(self, event: Input.Submitted) -> None:
        text = event.value.strip()
        event.input.clear()
        self.query_one(RichLog).write(Text(f"> {text}", "bold cyan"))
        match text.lower():
            case "quit" | "q":
                self.exit()
            case "save":
                self.action_save()
            case "restore":
                self.action_restore()
            case "undo":
                self.action_undo()
            case _:
                self.say(self.game.play(text))
        if self.game.over:
            self.push_screen(TheEnd(self.game.title), self.again)

    def again(self, wanted: bool | None) -> None:
        """Called with the answer, when the last screen has been dismissed."""
        if not wanted:
            self.exit()
            return
        self.game = self.new_game()
        self.begin()

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        """Textual asks this before it shows, or runs, any action."""
        match action:
            case "undo":
                return isinstance(self.game, Undoable)
            case "save" | "restore":
                return isinstance(self.game, Saveable)
            case _:
                return True

    def action_help(self) -> None:
        self.say(HELP + "\n" + self.game.play("help"))

    def action_save(self) -> None:
        if isinstance(self.game, Saveable):
            self.say(self.game.save(self.save_file))

    def action_restore(self) -> None:
        if isinstance(self.game, Saveable):
            self.say(self.game.restore(self.save_file))

    def action_undo(self) -> None:
        if isinstance(self.game, Undoable):
            self.say(self.game.undo())
