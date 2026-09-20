"""What the tests of the app do again and again."""

from textual.pilot import Pilot
from textual.widgets import Input, RichLog

from adventure.app import AdventureApp


async def say(pilot: Pilot[None], text: str) -> None:
    """Put a command in the prompt, and press Return."""
    pilot.app.query_one(Input).value = text
    await pilot.press("enter")


def story(app: AdventureApp) -> str:
    """Return everything in the log, as plain text."""
    return "\n".join(line.text for line in app.query_one(RichLog).lines)
