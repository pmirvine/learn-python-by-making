"""Project 6's Game of Life, running in a browser's tab. The rules aren't changed."""

import asyncio

from life import soup, step
from pyscript import document, when

WIDTH, HEIGHT = 160, 120

canvas = document.querySelector("#board")
pen = canvas.getContext("2d")
status = document.querySelector("#status")
live = soup(WIDTH, HEIGHT)
generation = 0


@when("click", "#again")
def start_again(event) -> None:
    global live, generation
    live = soup(WIDTH, HEIGHT)
    generation = 0


def draw() -> None:
    pen.fillStyle = "black"
    pen.fillRect(0, 0, WIDTH, HEIGHT)
    pen.fillStyle = "lime"
    for x, y in live:
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            pen.fillRect(x, y, 1, 1)


async def main() -> None:
    global live, generation
    while True:
        draw()
        status.textContent = f"Generation {generation}, with {len(live)} cells alive"
        live = step(live)
        generation += 1
        await asyncio.sleep(0.05)


await main()  # noqa: F704, PLE1142
