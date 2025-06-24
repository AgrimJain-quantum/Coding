from tkinter import *

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

# ---------------------------- SAVE PASSWORD ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(r"C:\Users\Agrim Jain\Desktop\Coding\python\password manager\logo.png")
canvas.create_image(100, 100, image=r"C:\Users\Agrim Jain\Desktop\Coding\python\password manager\logo.png")
canvas.grid(column=1, row=0)