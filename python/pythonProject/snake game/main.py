# to do
# create a snake body
# how to move the snake
# detect collision with food
# create a score board
# detect the collision with the wall
# detect the colision with the tail
from turtle import Screen
from snake import Snake  
from food import Food
import time
snake = Snake() 
food = Food()  # Create an instance of the Food class
screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)  
screen.listen()  
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")  
screen.onkey(snake.right, "Right")

 # Create an instance of the Snake class
game_is_on = True
while game_is_on:
    screen.update()  # Update the screen to show the snake
    time.sleep(0.1)  
    snake.move()
 
    

screen.exitonclick()
 