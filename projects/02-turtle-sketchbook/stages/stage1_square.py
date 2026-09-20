import turtle

screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")

pen = turtle.Turtle()
pen.color("yellow")
pen.pensize(3)

for _ in range(4):
    pen.forward(200)
    pen.left(90)

screen.mainloop()
