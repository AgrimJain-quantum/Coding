# Snake Game
from turtle import *
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
    if snake.head.distance(food) < 15:  
        food.refresh()
        snake.extend()
        scoreboard.increase_score()
       
    # Check for collision with wall
    if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 290 or snake.head.ycor() < -290:
        game_is_on = False
        scoreboard.goto(0, 0)
        scoreboard.write("Game Over", align="center", font=("Arial", 24, "normal"))
    # detect collision with the tail
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()
screen.exitonclick()   
screen.bye()

    