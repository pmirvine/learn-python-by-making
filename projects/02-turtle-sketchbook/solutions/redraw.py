"""Extend 3: press the space bar for a new tree. Every one is different."""

import random
import turtle

BARK = (120, 80, 40)
LEAF = (60, 160, 70)

screen = turtle.Screen()
pen = turtle.Turtle()


def tree(pen, length, depth):
    """Draw a tree: a branch, then two smaller trees growing from its tip."""
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


def new_tree():
    """Wipe the screen and grow another tree."""
    pen.clear()
    pen.penup()
    pen.goto(0, -280)
    pen.pendown()
    pen.setheading(90)
    tree(pen, 120, 8)
    screen.update()


def main():
    screen.setup(800, 600)
    screen.colormode(255)
    screen.bgcolor(10, 10, 40)
    screen.tracer(0)
    pen.hideturtle()

    new_tree()

    # No brackets after new_tree: this hands over the function itself, for
    # the screen to call later, whenever the space bar is pressed.
    screen.onkey(new_tree, "space")
    screen.listen()
    screen.mainloop()


if __name__ == "__main__":
    main()
