"""The line editor. Like the original's, it can add to the end, and take from the end."""

from micro.textscreen import RUB_OUT, TextScreen

LONGEST = 238  # as on the BBC Micro, which kept the line in one 256-byte page


class LineEditor:
    def __init__(self, screen: TextScreen) -> None:
        self.screen = screen
        self.line = ""

    def type(self, character: str) -> None:
        if character.isprintable() and len(self.line) < LONGEST:
            self.line += character
            self.screen.write(character)

    def rub_out(self) -> None:
        if self.line:
            self.line = self.line[:-1]
            self.screen.write(RUB_OUT)

    def take(self) -> str:
        """Return is pressed: hand over the line, and start another."""
        line, self.line = self.line, ""
        self.screen.write("\n")
        return line
