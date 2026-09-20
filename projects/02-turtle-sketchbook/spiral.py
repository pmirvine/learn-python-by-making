import turtle

COLOURS = ("red", "yellow", "green", "cyan", "blue", "magenta")

screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")

pen = turtle.Turtle()
pen.speed(0)
pen.pensize(2)

for step in range(100):
    pen.color(COLOURS[step % len(COLOURS)])
    pen.forward(step * 3)
    pen.left(61)

screen.mainloop()
