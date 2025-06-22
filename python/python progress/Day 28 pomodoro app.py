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
import time
def countdown(count):
    window.after(1000, countdown, count - 1)






# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx = 100, pady = 50, bg = YELLOW)
count
#title 
title_label = Label(text = "Timer", font = (FONT_NAME, 35, "bold"),fg =GREEN,bg = YELLOW)
title_label.grid(column=1, row=0)

#bg with clock
canvas  = Canvas(width=200, height=224, bg = YELLOW, highlightthickness = 0 ) 
PhotoImage = PhotoImage(file = r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\tomato.png")
canvas.create_image(100, 112, image = PhotoImage)
canvas.create_text(100, 130, text = "00:00", fill = "white", font = (FONT_NAME, 35, "bold"), tag = "timer")
canvas.grid(column=1, row=1)

#buttons
###start button
start = Button(text = "Start", font = (FONT_NAME, 10, "bold"), command = None, highlightthickness = 0)
start.grid(column = 0, row = 2)

###stop button
reset_button = Button(text = "reset", font = (FONT_NAME, 10, "bold"), command = None, highlightthickness = 0)
reset_button.grid(column = 2, row = 2)

#check mark
check_mark = Label(text = "✓", fg = GREEN, bg = YELLOW, font = (FONT_NAME, 30, "bold"))
check_mark.grid(column = 1, row = 3)




window.mainloop()