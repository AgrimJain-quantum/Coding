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
    time.sleep(0.1)  # Control the speed of the snake
    for segment in segments:
        segment.forward(20)
        screen.update()  
    











screen.exitonclick()
 