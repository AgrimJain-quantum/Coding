# to do
# create a snake body
# how to move the snake
# detect collision with food
# create a score board
# detect the collision with the wall
# detect the colision with the tail
from turtle import Turtle, Screen
import time
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)  # Turn off the screen updates for smoother animation
starting_position = [(0, 0), (-20, 0), (-40, 0)]
segments = []

for position in starting_position:
    segment = Turtle("square")
    segment.color("white")
    segment.penup()
    segment.goto(position)
    segments.append(segment)

game_is_on = True
while game_is_on:
    screen.update()  # Update the screen to show the snake
    time.sleep(0.1)  
    for seg_num in range(len(segments) - 1 , 0 , -1 ):
        new_x = segments[seg_num - 1].xcor()
        new_y = segments[seg_num - 1].ycor()
        segments[seg_num].goto(new_x, new_y)
    segments[0].forward(20)
    segments[0].left(90)  # Change direction to left for demonstration
    # Control the speed of the snake










screen.exitonclick()
 