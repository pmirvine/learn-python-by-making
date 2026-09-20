"""Tweak 2 and Extend 2: a tree you can adjust, in any season you like."""

import random
import turtle

BARK = (120, 80, 40)
SEASONS = ("spring", "summer", "autumn", "winter")


def leaf_colour(season):
    """Return an (r, g, b) colour for a leaf, or None when the tree is bare."""
    if season == "spring":
        return (255, random.randint(150, 220), 220)
    elif season == "summer":
        return (60, random.randint(130, 190), 70)
    elif season == "autumn":
        return (random.randint(200, 255), random.randint(80, 160), 20)
    return None


def tree(pen, length, depth, season="summer", spread=25, shrink=0.75):
    """Draw a tree, with a leaf or a blossom at the tip of every twig.

    spread is the average angle between a branch and its parent, and shrink is
    how much shorter each branch is than the one it grew from.
    """
    if depth == 0:
        colour = leaf_colour(season)
        if colour is not None:
            pen.dot(7, colour)
        return

    lean = random.uniform(spread - 10, spread + 10)
    pen.pensize(depth)
    pen.color(BARK)
    pen.forward(length)

    pen.left(lean)
    tree(pen, length * shrink, depth - 1, season, spread, shrink)
    pen.right(lean * 2)
    tree(pen, length * shrink, depth - 1, season, spread, shrink)
    pen.left(lean)

    pen.penup()
    pen.backward(length)
    pen.pendown()


def main():
    screen = turtle.Screen()
    screen.setup(800, 600)
    screen.colormode(255)
    screen.bgcolor(225, 235, 245)
    screen.tracer(10)

    pen = turtle.Turtle()
    pen.hideturtle()

    x = -292
    for season in SEASONS:
        pen.penup()
        pen.goto(x, -250)
        pen.pendown()
        pen.setheading(90)
        tree(pen, 54, 7, season=season, shrink=0.72)
        x += 195

    screen.update()
    screen.mainloop()


if __name__ == "__main__":
    main()
