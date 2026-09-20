import turtle


def koch(pen, length, depth):
    if depth == 0:
        pen.forward(length)
        return
    for angle in (60, -120, 60, 0):
        koch(pen, length / 3, depth - 1)
        pen.left(angle)


screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.tracer(20)

pen = turtle.Turtle()
pen.hideturtle()
pen.color("cyan")
pen.penup()
pen.goto(-240, 140)
pen.pendown()

for _ in range(3):
    koch(pen, 480, 4)
    pen.right(120)

screen.update()
screen.mainloop()
