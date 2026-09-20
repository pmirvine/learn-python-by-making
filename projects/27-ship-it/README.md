# beeb

`MOVE`, `DRAW`, `PLOT`, `SOUND` and `ENVELOPE`, for Python: the graphics and sound
commands of a BBC Micro, built on [pygame-ce](https://pyga.me).

![Eight colour bars, as on a television test card](https://raw.githubusercontent.com/yourname/beeb/main/docs/testcard.png)

The screen is 1280 by 1024, with the origin at the bottom left, whatever the size of
the window. There are eight colours, three channels of square waves, and one of noise.

## Try it

You need [uv](https://docs.astral.sh/uv/), and nothing else:

```console
$ uvx --from beeb-lpbm beeb
```

Eight bars and a beep mean that everything works. Escape closes the window.

## Use it

```console
$ uv add beeb-lpbm
```

```python
import beeb

beeb.mode(2)
beeb.gcol(0, 3)  # yellow
beeb.move(0, 0)
beeb.draw(1279, 1023)  # corner to corner
beeb.sound(1, -15, 53, 20)  # middle C, for a second

while True:
    beeb.vsync()
```

| | |
|---|---|
| `mode(n)` | open the screen: mode 0, 1, 2, 4 or 5 |
| `gcol(how, colour)`, `clg()` | choose a colour; clear the screen |
| `move(x, y)`, `draw(x, y)`, `plot(k, x, y)` | lines, points and filled triangles |
| `point(x, y)` | which colour is there? |
| `sound(channel, amplitude, pitch, duration)` | a note. Pitch is in quarter semitones, and 53 is middle C |
| `envelope(n, attack, decay, sustain, release)` | a shape for notes, used as amplitude `n` |
| `inkey()`, `mouse()`, `vsync()` | keys, the mouse, and the end of a frame |

There are longer examples in [`examples/`](https://github.com/yourname/beeb/tree/main/examples).

## Versions

beeb follows [semantic versioning](https://semver.org). Everything in `beeb.__all__` is
the public interface, and won't change in a way that breaks your programs before 2.0.
What has changed is in the [changelog](https://github.com/yourname/beeb/blob/main/CHANGELOG.md).

## Working on it

```console
$ git clone https://github.com/yourname/beeb
$ cd beeb
$ uv sync
$ uvx pre-commit install
$ uv run pytest
```

## Licence

[MIT](https://github.com/yourname/beeb/blob/main/LICENSE). "BBC" is a trade mark of
the British Broadcasting Corporation, with which this project has nothing to do.
