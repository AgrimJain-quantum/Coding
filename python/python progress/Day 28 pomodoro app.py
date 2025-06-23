from tkinter import * 
import time
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#f10b0b"
GREEN = "#00ad2b"
YELLOW = "#f3df04"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
# ---------------------------- TIMER RESET ------------------------------- # 

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    if reps % 8 == 0:
        countdown(long_break_sec)
    elif reps % 2 == 0:
        countdown(short_break_sec)
    else:
        countdown(work_sec)
    

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def countdown(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    canvas.itemconfig(timer_text, text = f"{count_min:02d}:{count_sec:02d}")
    if count > 0:
       window.after(1000, countdown, count - 1)





# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx = 100, pady = 50, bg = YELLOW)

#title 
title_label = Label(text = "Timer", font = (FONT_NAME, 35, "bold"),fg =GREEN,bg = YELLOW)
title_label.grid(column=1, row=0)

#bg with clock
canvas  = Canvas(width=200, height=224, bg = YELLOW, highlightthickness = 0 ) 
PhotoImage = PhotoImage(file = r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\tomato.png")
canvas.create_image(100, 112, image = PhotoImage)
timer_text = canvas.create_text(100, 130, text = "00:00", fill = "white", font = (FONT_NAME, 35, "bold"), tag = "timer")
canvas.grid(column=1, row=1)


#buttons
###start button
start = Button(text = "Start", font = (FONT_NAME, 10, "bold"), command = start_timer, highlightthickness = 0)
start.grid(column = 0, row = 2)

###stop button
reset_button = Button(text = "reset", font = (FONT_NAME, 10, "bold"), command = None, highlightthickness = 0)
reset_button.grid(column = 2, row = 2)

#check mark
check_mark = Label(text = "✓", fg = GREEN, bg = YELLOW, font = (FONT_NAME, 30, "bold"))
check_mark.grid(column = 1, row = 3)





window.mainloop()