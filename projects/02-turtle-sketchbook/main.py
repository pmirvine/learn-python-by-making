"""Turtle Sketchbook: pictures drawn by a turtle."""

import random
import turtle

NIGHT = (10, 10, 40)
MOONLIGHT = (255, 250, 205)
BARK = (120, 80, 40)
LEAF = (60, 160, 70)


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


def jump(pen, position):
    """Move to position, an (x, y) tuple, without drawing a line."""
    pen.penup()
    pen.goto(position)
    pen.pendown()


def random_position(screen):
    """Return a random (x, y) in the top two-thirds of the window."""
    half_width = screen.window_width() // 2
    half_height = screen.window_height() // 2
    x = random.randint(-half_width, half_width)
    y = random.randint(-half_height // 3, half_height)
    return x, y


def star(pen, position, size=None):
    """Draw a five-pointed star. Left to itself, it chooses its own size."""
    if size is None:
        size = random.randint(4, 16)
    jump(pen, position)
    for _ in range(5):
        pen.forward(size)
        pen.right(144)


def tree(pen, length, depth):
    """Draw a tree: a branch, then two smaller trees growing from its tip.

    Leaves the pen exactly where it found it, facing the same way.
    """
    if depth == 0:
        return

    lean = random.uniform(15, 35)
    pen.pensize(depth)
    pen.color(BARK if depth > 3 else LEAF)
    pen.forward(length)

    pen.left(lean)
    tree(pen, length * 0.75, depth - 1)
    pen.right(lean * 2)
    tree(pen, length * 0.75, depth - 1)
    pen.left(lean)

    pen.penup()
    pen.backward(length)
    pen.pendown()


def main():
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.colormode(255)
    screen.bgcolor(NIGHT)
    screen.tracer(10)

    pen = turtle.Turtle()
    pen.hideturtle()

    pen.color("white")
    for _ in range(60):
        star(pen, random_position(screen))

    pen.color(MOONLIGHT)
    jump(pen, (250, 170))
    rosette(pen, 18, sides=6, length=30)

    for x, height in ((-260, 70), (-20, 105), (240, 85)):
        jump(pen, (x, -290))
        pen.setheading(90)
        tree(pen, height, 8)

    screen.update()
    screen.mainloop()


if __name__ == "__main__":
    main()
