# detect collision with food
# create a score board
# detect the collision with the wall
# detect the colision with the tail
from turtle import Screen, Turtle
from snake import Snake  
from food import Food
import time
from scoreboard import Scoreboard

snake = Snake() 
food = Food() 
scoreboard = Scoreboard() 
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


game_is_on = True
while game_is_on:
    screen.update()  
    time.sleep(0.1)  
    snake.move()
    # Check for collision with food
    if snake.head.distance(food) < 15:  # Assuming food is a Turtle object
        food.refresh()  # Move food to a new random position
        new_segment = Turtle("square")
        new_segment.color("white")
        new_segment.penup()
        snake.segments.append(new_segment)  # Add a new segment to the snake

screen.exitonclick()
 