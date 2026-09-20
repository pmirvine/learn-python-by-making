from rich.console import Console

from shout import boxed


def test_it_shouts():
    console = Console(record=True, width=40)
    console.print(boxed(["ship", "it"]))
    assert "SHIP IT!" in console.export_text()
