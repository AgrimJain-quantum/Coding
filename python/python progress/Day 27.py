import tkinter as tk
from tkinter import *
window = tk.Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)

#label
my_label = tk.Label(text="I am a label", font=("Arial", 24, "bold", "italic"))
my_label.config(text = "New Text Again")
my_label.grid(column=0, row=0)



#button
def button_clicked():
    print("I got clicked")
    new_text = input.get()
    my_label.config(text= new_text)       
button = Button(text = "Click Me", command=button_clicked, font=("Arial", 24, "bold", "italic"))
button.grid(column=1, row=1 )

#entry
input = Entry(width = 10)
input.grid(column=2, row=2)
print(input.get()  ) 








window.mainloop()
    