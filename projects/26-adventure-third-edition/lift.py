from adventure.app import AdventureApp

FLOORS = ["the car park", "Haberdashery", "Toys", "the roof garden"]


class Lift:
    title = "Going Up"

    def __init__(self) -> None:
        self.floor = 0

    @property
    def over(self) -> bool:
        return self.floor == len(FLOORS) - 1

    def opening(self) -> str:
        return "You're in a lift, in " + FLOORS[self.floor] + ". Try: up, down."

    def play(self, text: str) -> str:
        step = {"up": 1, "down": -1}.get(text.strip().lower(), 0)
        if not step or not 0 <= self.floor + step < len(FLOORS):
            return "The lift doesn't budge."
        self.floor += step
        return f"Ding! The doors open on {FLOORS[self.floor]}."

    def status(self) -> dict[str, str]:
        return {"Floor": FLOORS[self.floor]}


AdventureApp(Lift).run()
