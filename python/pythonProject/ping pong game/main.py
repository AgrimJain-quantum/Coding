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
from turtle import *
screen = Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("Ping Pong Game")
paddle = Turtle()
paddle.shape("square")
paddle.shapesize(stretch_wid=5, stretch_len=1)
paddle.penup()
paddle.goto(350, 0)


screen.exitonclick()  