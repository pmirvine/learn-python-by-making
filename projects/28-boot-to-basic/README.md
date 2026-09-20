# micro

A home computer that never was. It boots to BASIC, draws with `MOVE` and `DRAW`, plays
`SOUND` and `ENVELOPE`, and has sprites, with collision detection, which the machine
that inspired it never had.

![A black screen: Python Micro 64K, Tiny BASIC, a three-line program, its listing, and what it printed](https://raw.githubusercontent.com/yourname/micro/main/docs/hello.png)

It's the last project of [Learn Python by Making](https://github.com/pmirvine/learn-python-by-making),
and it's made of the others: the BASIC interpreter from Project 17, the graphics and
sound of `beeb`, the teletext page from PyFax, and the sprite files of the sprite editor.

## Try it

```console
$ uv run micro
```

```text
>10 MODE 1
>20 FOR X=0 TO 1279 STEP 16
>30 MOVE X,0: DRAW 1279-X,1023
>40 NEXT
>RUN
```

Escape stops a program. `CAT` lists the disc, which is the folder `disc/`, stocked
with a few programs the first time that you switch on. `LOAD "alien"` fetches a game.

## What it adds to the BASIC

| | |
|---|---|
| `MODE n`, `CLS`, `CLG`, `COLOUR n`, `GCOL a, c` | the screen |
| `MOVE x, y`, `DRAW x, y`, `PLOT k, x, y` | graphics, on a screen 1280 by 1024, from the bottom left |
| `SOUND c, a, p, d`, `ENVELOPE n, a, d, s, r` | three channels of square waves, and one of noise |
| `SPRITE n, "name"`, `PUT n, x, y`, `HIDE n` | sprites, from `.sprite` files on the disc |
| `COLLIDE(a, b)`, `EDGE(n)` | are two sprites touching? Is one over the edge? |
| `INKEY(-98)`, `INKEY(0)`, `TAB(x, y)`, `WAIT` | keys, the text cursor, and the end of a frame |

## Licence

[MIT](https://github.com/yourname/micro/blob/main/LICENSE).
