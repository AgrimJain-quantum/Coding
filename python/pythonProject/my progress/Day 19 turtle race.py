from turtle import Turtle, Screen

screen = Screen()
screen.setup(width=500, height = 400)
user_bet = screen.textinput(title = "make your bet" , prompt = "Which turtle will win the race? Enter a color:")
color = ["red", "orange", "yellow", "green", "blue", "purple"]
y_positions = [-70, -40, -10, 20, 50, 80]

for turtle_index in range(0, 6):
    tim = Turtle(shape = "turtle")
    tim.color(color[turtle_index])
    tim.penup()
    tim.goto(x = -230, y = y_positions[turtle_index])
if 


screen.exitonclick()