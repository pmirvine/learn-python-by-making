"""What goes wrong in a BASIC program, said as the BBC Micro would have said it."""


class BasicError(Exception):
    """A mistake in somebody's BASIC. The message is what they'll be shown."""

    def __init__(self, message: str, line: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.line = line

    def __str__(self) -> str:
        if self.line is None:
            return self.message
        return f"{self.message} at line {self.line}"
