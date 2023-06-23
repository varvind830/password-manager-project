from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = ''.join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(text=password)

# ---------------------------- SEARCH WEBSITE ------------------------------- #

def find_password():
    website_text = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="File Not Found", message="No Data File Found.")

    else:
        if website_text in data:
            username = data[website_text]["username"]
            password = data[website_text]["password"]

            messagebox.showinfo(title=website_entry.get(), message=f"Username: {username}\n"
                                                                   f"Password: {password}")
        else:
            messagebox.showinfo(title=website_entry.get(), message="No details for the website exists.")


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website_text = website_entry.get()
    username_text = username_entry.get()
    password_text = password_entry.get()
    new_data = {website_text: {
        "username": username_text,
        "password": password_text,
    }
    }

    if len(username_text) == 0 or len(password_text) == 0:
        messagebox.showinfo(title="Error", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(first=0, last=END)
            password_entry.delete(first=0, last=END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry()
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()

username_entry = Entry()
username_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
username_entry.insert(0, "varvind@email.com")

password_entry = Entry()
password_entry.grid(column=1, row=3, sticky="EW")

# Buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="EW")

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3, sticky="EW")

add_button = Button(text="Add", command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW")

window.mainloop()
