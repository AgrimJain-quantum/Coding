# to do
# create a snake body
# how to move the snake
# detect collision with food
# create a score board
# detect the collision with the wall
# detect the colision with the tail
from turtle import Turtle, Screen
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")


starting_position = [(0, 0), (-20, 0), (-40, 0)]


for position in starting_position:
    segment = Turtle("square")
    segment.color("white")
    segment.penup()
    segment.goto(position)
    segment.speed("fastest")
    segment.stamp()  # Stamp the turtle to leave a mark
    segment.hideturtle()  # Hide the turtle after stamping
# segment_1 = Turtle("square")
# segment_1.color("white")
# segment_1.goto(0, 0)
# segment_2 = Turtle("square")
# segment_2.color("white")
# segment_2.goto(-20, 0)
# segment_3 = Turtle("square")
# segment_3.color("white")
# segment_3.goto(-40, 0)
# segment_1.speed("fastest")
# segment_1.penup()
# segment_2.penup()
# segment_3.penup()





screen.exitonclick()
 