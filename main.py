from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import json


def generate():
    # Password generator
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password = [choice(letters) for i in range(randint(6, 8))] + [choice(numbers) for k in range(randint(2, 4))] + [choice(symbols) for m in range(randint(2, 4))]

    shuffle(password)
    password = ''.join(password)

    entry_password.delete(0, END)
    entry_password.insert(string=password, index=0)


def save():
    # Saving password to a .json file
    fields = []
    for entry in [entry_website, entry_email, entry_password]:
        fields.append(entry.get())

    if len(fields[0]) == 0 or len(fields[1]) == 0 or len(fields[2]) == 0:
        messagebox.showinfo(title="Empty field detected", message="Please fill in all the fields.")
    else:
        is_ok = messagebox.askokcancel(title=fields[0],
                                       message=f'These are the details entered: \nEmail: {fields[1]}\nPassword: {fields[2]}\nSave?')
        if is_ok:
            for entry in [entry_website, entry_email, entry_password]:
                if entry != entry_email:
                    entry.delete(0, END)

            new_data = {
                fields[0]: {
                    'email': fields[1],
                    'password': fields[2]
                }
            }

            try:
                with open('data.json', 'r') as f:
                    data = json.load(f)
            except (json.decoder.JSONDecodeError, FileNotFoundError):
                with open('data.json', 'w') as f:
                    json.dump(new_data, f, indent=4)
            else:
                data.update(new_data)
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)


def search():
    # Look-up in the .json file of passwords
    search_website = entry_website.get()
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        messagebox.showinfo(title="Nope", message="File not found.")
    else:
        if search_website in data:
            final_data = json.dumps(data[search_website], indent=4).replace('"', '').replace('{', '').replace('}', '')
            messagebox.showinfo(title=search_website, message=final_data)
        else:
            messagebox.showinfo(title="No :(", message="No details for this website.")


# UI setup
window = Tk()
window.title('Password manager')
window.config(padx=20, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# Labels
website = Label(text='Website:', font=('Arial', 10))
website.grid(column=0, row=1, sticky='e')

email = Label(text='Email/Username:', font=('Arial', 10))
email.grid(column=0, row=2, sticky='e')

password_lbl = Label(text='Password:', font=('Arial', 10))
password_lbl.grid(column=0, row=3, sticky='e')

# Entries
entry_website = Entry(width=25)
entry_website.grid(column=1, row=1)
entry_website.focus()

entry_email = Entry(width=40)
entry_email.grid(column=1, row=2, columnspan=2)

entry_password = Entry(width=25)
entry_password.grid(column=1, row=3, padx=0)

# Buttons
button_generate = Button(text='Generate password', font=('Arial', 8), width=14, command=generate)
button_generate.grid(column=2, row=3, padx=0)

button_add = Button(text='Add', font=('Arial', 8), width=40, command=save)
button_add.grid(column=1, row=4, columnspan=2)

button_search = Button(text='Search', font=('Arial', 8), width=14, command=search)
button_search.grid(column=2, row=1)

window.mainloop()
