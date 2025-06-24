#----------------------ui setup----------------------#
from tkinter import *
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file=r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\logo_image.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)




















































window.mainloop()
