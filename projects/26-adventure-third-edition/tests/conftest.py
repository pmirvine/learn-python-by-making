"""Things that every test file may want: a game to win, and a game to test with."""

WALKTHROUGH = [
    "s", "e", "take torch", "s", "examine flowerpots", "take key", "n", "w",
    "unlock door", "w", "take cassette", "e", "u", "u", "load cassette",
]  # fmt: skip


class Parrot:
    """The smallest game there could be. It inherits from nothing."""

    title = "Parrot"

    def __init__(self) -> None:
        self.heard: list[str] = []

    @property
    def over(self) -> bool:
        return "bye" in self.heard

    def opening(self) -> str:
        return "Pretty Polly."

    def play(self, text: str) -> str:
        self.heard.append(text)
        return f"Squawk! {text}!"

    def status(self) -> dict[str, str]:
        return {"Heard": str(len(self.heard))}
