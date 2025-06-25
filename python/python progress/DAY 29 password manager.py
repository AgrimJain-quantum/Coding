#----------------------ui setup----------------------#
from tkinter import *
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file=r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\logo_image.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

#labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1, sticky="W")

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2, sticky="W")

password_label = Label(text="Password:")
password_label.grid(column=0, row=3, sticky="W")
#entries
website_entry = Entry(width=43)
email_entry = Entry(width=43)
password_entry = Entry(width=21)

website_entry.grid(column=1, row=1, columnspan = 2, sticky = "W")
email_entry.grid(column=1, row=2, columnspan = 2, sticky = "W")
password_entry.grid(column=1, row=3, sticky = "W")

#buttons
generate_password_button = Button(text = "Generate Password")
add_button = Button(text = "Add", width=36)

generate_password_button.grid(column=2, row=3, sticky="W")
add_button.grid(column=1, row=4, columnspan=2, sticky="W")

















































window.mainloop()
