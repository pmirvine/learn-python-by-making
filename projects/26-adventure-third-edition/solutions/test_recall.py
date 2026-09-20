from recall import Prompt
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Input


class Desk(App[None]):
    def compose(self) -> ComposeResult:
        yield Prompt(placeholder="What now?")

    @on(Input.Submitted)
    def clear(self, event: Input.Submitted) -> None:
        event.input.clear()


async def test_up_and_down_go_through_the_past():
    app = Desk()
    async with app.run_test() as pilot:
        prompt = app.query_one(Prompt)
        for command in ["north", "take torch", "take torch", " "]:
            prompt.value = command
            await pilot.press("enter")
        assert prompt.past == ["north", "take torch"]

        await pilot.press("up")
        assert prompt.value == "take torch"
        await pilot.press("up", "up", "up")
        assert prompt.value == "north"
        await pilot.press("down", "down")
        assert prompt.value == ""
