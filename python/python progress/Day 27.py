import tkinter as tk
from tkinter import Button
window = tk.Tk()
window.title("My First GUI Program")
window.minsize(width=500, height=300)

#label
my_label = tk.Label(text="I am a label", font=("Arial", 24, "bold", "italic"))
my_label.pack(expand = True)
my_label["text"] = "New Text"
my_label.config(text = "New Text Again")

#button

def button_clicked():
    print("I got clicked")
    my_label.config(text="I got clicked")


    
button = Button(text = "Click Me", command=button_clicked, font=("Arial", 24, "bold", "italic"))
button.pack(expand = True)














window.mainloop()
    