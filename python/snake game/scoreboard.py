from turtle import Turtle
ALIGN = "center"
FONT = ("Arial", 24, "normal")
class Scoreboard (Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.highscore = 0
        
        self.color("white")
        self.penup()
        self.goto(0, 270) 
        self.hideturtle()
        self.update_scoreboard()
        
    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score}", align = ALIGN, font = FONT)
    
    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.update_scoreboard()
        
    # def game_over(self):
    #     self.goto(0, 0)
    #     self.write("Game Over", align = ALIGN, font = FONT)
        
        
    def increase_score(self):   
        self.score += 1
        self.update_scoreboard()