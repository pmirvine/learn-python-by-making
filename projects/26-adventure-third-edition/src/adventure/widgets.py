"""The panels at the side of the story: the map, and a few facts."""

from rich.text import Text
from textual.reactive import reactive
from textual.widgets import Static

from adventure.chart import draw
from adventure.game import Chart


class MapPanel(Static):
    """The floor that the player is on, redrawn whenever it's given a new chart."""

    chart: reactive[Chart | None] = reactive(None)

    def watch_chart(self, chart: Chart | None) -> None:
        if chart is not None:
            self.border_title = chart.caption or "Map"
            self.update("\n".join(draw(chart)))


class StatusPanel(Static):
    """A short list of names and values."""

    facts: reactive[dict[str, str]] = reactive(dict[str, str])

    def watch_facts(self, facts: dict[str, str]) -> None:
        lines = [
            Text.assemble((f"{name}: ", "bold"), value) for name, value in facts.items()
        ]
        self.update(Text("\n").join(lines))
