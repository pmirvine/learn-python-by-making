"""Turtle Sketchbook: pictures drawn by a turtle."""

import turtle


def polygon(pen, sides, length=100):
    """Draw a regular polygon, ending where it started, facing the same way."""
    for _ in range(sides):
        pen.forward(length)
        pen.left(360 / sides)


def rosette(pen, petals, sides=4, length=100):
    """Draw a ring of polygons, turning a little between each."""
    for _ in range(petals):
        polygon(pen, sides, length)
        pen.left(360 / petals)


def main():
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.bgcolor("black")

    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("cyan")

    rosette(pen, 36, sides=6, length=90)

    screen.mainloop()


if __name__ == "__main__":
    main()
