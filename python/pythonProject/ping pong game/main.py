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
from turtle import Screen, Turtle
from paddle import Paddle
screen = Screen()
screen.bgcolor("black")
screen.setup(width = 800, height= 600)
screen.title("Pong Game")  

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))


    
screen.listen()
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")
screen.onkey(l_paddle.go_up, "w")
screen.onkey(l_paddle.go_down, "s")

game_is_on = True
while game_is_on:
    screen.update()
    

screen.exitonclick()
