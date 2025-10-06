from tkinter import *
from tkinter import messagebox
from random import *
import json
#---------------------password generator function---------------------#
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    
#----------------------save password function----------------------#

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website:{
            "email" : email,
            "password" : password
        }
    }
    
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title = "Error" , message = "please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                #json.dump(new_data, data_file, indent = 4)
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent = 4)
            
        else:   
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent = 4)
        finally:        
            website_entry.delete(0, END)
            password_entry.delete(0, END)


#----------------------ui setup----------------------#
def find_password():
    website = website_entry.get()
    with open("data.json") as data_file:
        data = json.load(data_file)
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")
             
             









#----------------------ui setup----------------------#

window = Tk()
window.title("Password Manager")
window.config(padx=70, pady=70)

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
website_entry = Entry(width=35)
email_entry = Entry(width=43)
password_entry = Entry(width=24)
website_entry.grid(column=1, row=1, columnspan = 2, sticky = "W")
email_entry.grid(column=1, row=2, columnspan = 2, sticky = "W")
password_entry.grid(column=1, row=3, sticky = "W")
website_entry.focus()
email_entry.insert(0, "agrimjain015@gmail.com")
#buttons
search_button = Button(text = "Search", command = find_password)
generate_password_button = Button(text = "Generate Password", command = generate_password)
add_button = Button(text = "Add", width=36, command = save)
search_button.grid(column=2, row=1, sticky="E") 
generate_password_button.grid(column=1, row=3,columnspan=2,sticky="E") 
add_button.grid(column=1, row=4, columnspan=2, sticky="W")




window.mainloop()