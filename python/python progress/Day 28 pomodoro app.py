#TODO
#WE HAVE TO CREATE A POMODORO TIMER APP
# FLOW OF THE APP
#4 * 25 MINUTES WORK
#3* 5 MINUTES BREAK
#1 * 20 MINUTES BREAK
#1. Create a window with a title
#2. Create a canvas with a tomato image
#3. Create a label to show the timer
#4. Create a start button to start the timer
#5. Create a reset button to reset the timer

from tkinter import * 
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#f10b0b"
GREEN = "#00ad2b"
YELLOW = "#f3df04"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# ---------------------------- TIMER RESET ------------------------------- # 

# ---------------------------- TIMER MECHANISM ------------------------------- # 

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx = 100, pady = 50)
canvas  = Canvas(width=200, height=224) 
PhotoImage = PhotoImage(file = r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\tomato.png")
canvas.create_image(102, 112, image = PhotoImage)
canvas.create_text(102, 130, text = "00:00", fill = "white", font = (FONT_NAME, 35, "bold"), tag = "timer")
canvas.pack()






window.mainloop()
