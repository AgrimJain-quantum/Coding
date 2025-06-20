import tkinter as tk
from tkinter import *
window = tk.Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)

#label
my_label = tk.Label(text="I am a label", font=("Arial", 24, "bold", "italic"))
my_label.pack(side = "left")
my_label["text"] = "New Text"
my_label.config(text = "New Text Again")

#button
def button_clicked():
    print("I got clicked")
    new_text = input.get()
    my_label.config(text= new_text)       
button = Button(text = "Click Me", command=button_clicked, font=("Arial", 24, "bold", "italic"))
button.pack(side = "bottom")

#entry
input = Entry(width = 10)
input.pack(side = "right")
print(input.get()  ) 








window.mainloop()
    