'''ping pong game
This is a simple ping pong game using the turtle module in Python.
create the screen
create and move a paddle
create another paddle
create the ball and make it move
detect collision with the paddle
detect collision with the wall and bounce
detect when paddle misses the ball
keep the score
'''
from turtle import Screen
screen = Screen()
screen.bgcolor("black")
screen.setup(width = 800, height= 600)
screen.title("Ping Pong Game")  




screen.exitonclick()
