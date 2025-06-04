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
screen = Screen()
screen.bgcolor("black")
screen.setup(width = 800, height= 600)
screen.title("Pong Game")  

paddle = Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=5, stretch_len=1)
paddle.penup()
paddle.goto(350,0)

def go_up():
    new_y = paddle.ycor() + 20
    paddle.goto(paddle.xcor(), new_y)
def go_down():
    new_y = paddle.ycor() - 20
    paddle.goto(paddle.xcor(), new_y)
    


screen.listen()
screen.onkey(go_up(), "Up")
screen.onkey(go_down(), "Down")

screen.exitonclick()
