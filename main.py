import os
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

def run_home():
    os.system("python3 home.py")

def check_password():
    saved_password = "1234567890"

    entered_password = simpledialog.askstring("Password", "Enter the password:", show='*')

    if entered_password == saved_password:
        run_home()
    else:
        messagebox.showerror("Error", "Incorrect password")


root = tk.Tk()
root.withdraw() 

check_password()

root.mainloop()
