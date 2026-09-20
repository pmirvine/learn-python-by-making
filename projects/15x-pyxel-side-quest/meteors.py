"""Meteors: a complete game for the Pyxel fantasy console."""

from pathlib import Path

import pyxel

SIZE = 128
SHIP_Y = SIZE - 20
# Your sprite files use the BBC's colours. These are the nearest that Pyxel has,
# and its colour 15 will stand for see-through.
BBC_TO_PYXEL = str.maketrans(".01234567", "f08ba52c7")
CLEAR = 15


def load_sprite(path: Path, image: int) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    rows = [line for line in lines if line and line[0] in ".01234567"]
    pyxel.images[image].set(0, 0, [row.translate(BBC_TO_PYXEL) for row in rows])


class Game:
    def __init__(self) -> None:
        pyxel.init(SIZE, SIZE, title="Meteors", fps=30)
        load_sprite(Path(__file__).parent / "rocket.sprite", 0)
        pyxel.sounds[0].set("c3g3", "p", "4", "n", 6)
        pyxel.sounds[1].set("c2a1f1c1", "n", "7654", "f", 12)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self) -> None:
        self.x = SIZE // 2 - 8
        self.meteors: list[list[float]] = []
        self.score = 0
        self.alive = True

    def update(self) -> None:
        if not self.alive:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset()
            return

        self.x += 2 * (pyxel.btn(pyxel.KEY_RIGHT) - pyxel.btn(pyxel.KEY_LEFT))
        self.x = max(0, min(SIZE - 16, self.x))
        if pyxel.frame_count % 8 == 0:
            self.meteors.append([pyxel.rndi(0, SIZE), -4, pyxel.rndf(1, 3)])

        for meteor in self.meteors:
            meteor[1] += meteor[2]
            if abs(meteor[0] - self.x - 8) < 7 and abs(meteor[1] - SHIP_Y - 8) < 7:
                self.alive = False
                pyxel.play(0, 1)
        fallen = [meteor for meteor in self.meteors if meteor[1] > SIZE]
        if fallen and self.alive:
            self.score += len(fallen)
            pyxel.play(0, 0)
        self.meteors = [meteor for meteor in self.meteors if meteor[1] <= SIZE]

    def draw(self) -> None:
        pyxel.cls(1 if self.alive else 2)
        for n in range(30):
            pyxel.pset(n * 37 % SIZE, (n * 53 + pyxel.frame_count) % SIZE, 13)
        for x, y, _speed in self.meteors:
            pyxel.circ(x, y, 3, 9)
            pyxel.circ(x - 1, y - 1, 1, 10)
        pyxel.blt(self.x, SHIP_Y, 0, 0, 0, 16, 16, CLEAR)
        pyxel.text(4, 4, f"SCORE {self.score}", 7)
        if not self.alive:
            pyxel.text(34, 56, "SPACE TO RETRY", pyxel.frame_count % 16)


Game()
