from turtle import Turtle
class Scoreboard (Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.write(f"Score: {self.score}", align="center", font=("Arial", 24, "normal"))
        self.hideturtle()
        self.goto(0, 260)  # Position the scoreboard at the top of the screen
        
    