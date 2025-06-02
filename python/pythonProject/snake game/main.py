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




game_is_on = True
while game_is_on:
    screen.update()  # Update the screen to show the snake
    time.sleep(0.1)  
  # Change direction to left for demonstration
    # Control the speed of the snake










screen.exitonclick()
 