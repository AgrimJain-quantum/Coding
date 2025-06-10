import turtle
import pandas as pd

screen = turtle.Screen()
screen.title("States Game")
image_path = r"C:\Users\Agrim Jain\Desktop\Coding\python\states game\blank_states_img.gif"
screen.addshape(image_path)
turtle.shape(image_path)
screen.setup(width=725, height=491)

answer_state = screen.textinput(title = "Guess the state" , prompt = "What's another state's name?").title()

data = pd.read_csv(r"C:\Users\Agrim Jain\Desktop\Coding\python\states game\50_states.csv")
state_list = data.state.to_list()
print(state_list)
if answer_state in state_list:
    t = turtle.Turtle()
    t.hideturtle()
    t.penup()
    state_data = data[data.state == answer_state]
    t.goto(state_data.x.item(), state_data.y.item())
    t.write(state_data.state)
    
    
# if answerr_state is one of the states in all the states of the 50_states.csv file
        #if they got it right 
           #create a turtle to write the state name at the state's x and y coordinates





screen.exitonclick()
