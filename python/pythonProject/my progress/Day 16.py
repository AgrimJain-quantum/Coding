# import turtle
# timmy = turtle.Turtle()
# def draw_square(size):
#     for _ in range(4):
#         timmy.forward(size)
#         timmy.right(90)

# def draw_dashed_line(length, dash_length):
#     for _ in range(length // (2 * dash_length)):
#         timmy.forward(dash_length)
#         timmy.penup()
#         timmy.forward(dash_length)
#         timmy.pendown()

from turtle import Turtle , Screen
my_screen = Screen()
timmy = Turtle()
print(my_screen.canvheight)
timmy.shape("turtle")
timmy.color("red")
print(timmy)
my_screen.exitonclick()