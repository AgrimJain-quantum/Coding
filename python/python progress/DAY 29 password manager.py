# #----------------------ui setup----------------------#
# from tkinter import *
# window = Tk()
# window.title("Password Manager")
# window.config(padx=50, pady=50)

# canvas = Canvas(width=200, height=200)
# logo_img = PhotoImage(file=r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\logo_image.png")
# canvas.create_image(100, 100, image=logo_img)
# canvas.grid(column=1, row=0)

# #labels
# website_label = Label(text="Website:")
# website_label.grid(column=0, row=1, sticky="W")

# email_label = Label(text="Email/Username:")
# email_label.grid(column=0, row=2, sticky="W")

# password_label = Label(text="Password:")
# password_label.grid(column=0, row=3, sticky="W")
# #entries
# website_entry = Entry(width=43)
# email_entry = Entry(width=43)
# password_entry = Entry(width=26)

# website_entry.grid(column=1, row=1, columnspan = 2, sticky = "W")
# email_entry.grid(column=1, row=2, columnspan = 2, sticky = "W")
# password_entry.grid(column=1, row=3, sticky = "W")

# #buttons
# generate_password_button = Button(text = "Generate Password")
# add_button = Button(text = "Add", width=36)

# generate_password_button.grid(column=2, row=3)
# add_button.grid(column=1, row=4, columnspan=2, sticky="W")



from tkinter import *
# Optional: from PIL import Image, ImageTk

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# Canvas
canvas = Canvas(width=220, height=220, highlightthickness=0)
logo_img = PhotoImage(file=r"C:\Users\Agrim Jain\Desktop\Coding\python\python progress\logo_image.png")
canvas.create_image(110, 110, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1, sticky="W", pady=5)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2, sticky="W", pady=5)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3, sticky="W", pady=5)

# Entry fields
website_entry = Entry(width=43)
website_entry.grid(column=1, row=1, columnspan=2)

email_entry = Entry(width=43)
email_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=26)
password_entry.grid(column=1, row=3)

# Buttons
generate_password_button = Button(text="Generate Password")
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36)
add_button.grid(column=1, row=4, columnspan=2, pady=10)

window.mainloop()














































# window.mainloop()
