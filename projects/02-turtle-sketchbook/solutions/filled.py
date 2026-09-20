"""Extend 1: polygons that can be filled, chosen with a keyword argument."""

import turtle

COLOURS = ("red", "yellow", "green", "cyan", "blue", "magenta")


def polygon(pen, sides, length=100, fill=None):
    """Draw a regular polygon. Give fill a colour to have it filled in."""
    if fill is not None:
        pen.fillcolor(fill)
        pen.begin_fill()
    for _ in range(sides):
        pen.forward(length)
        pen.left(360 / sides)
    if fill is not None:
        pen.end_fill()


def main():
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.bgcolor("black")

    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")

    # Biggest first, so that each smaller one is drawn on top of the last.
    for sides in range(8, 2, -1):
        polygon(pen, sides, 90, fill=COLOURS[sides % len(COLOURS)])

    screen.mainloop()


if __name__ == "__main__":
    main()
