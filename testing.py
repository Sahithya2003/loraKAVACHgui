import tkinter as tk
import gui

def show_home_page(root):
    # Code to display the Home page
    label = tk.Label(root, text="Welcome to the Home Page!", bg="#333", fg="white")
    label.grid(row=0, column=0, padx=20, pady=20)

def home_button_clicked(root):
    # Define the action to be taken when the button on the Home page is clicked
    # Redirect to Lora page
    switch_to_lora_page(root)

def create_main_gui():
    root = tk.Tk()
    root.title("Your App Name")
    root.config(bg="#333")  # Apply dark theme background color

    # Make the main window responsive
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Create a navigation bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Create a "File" menu with "Home" and "Lora" options
    file_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Home", command=lambda: switch_to_home_page(root))
    file_menu.add_command(label="Lora", command=lambda: switch_to_lora_page(root))

    # Create an "Exit" option in the "File" menu to quit the app
    file_menu.add_command(label="Exit", command=root.quit)

    # Show the Home page by default
    switch_to_home_page(root)

    root.mainloop()

def switch_to_home_page(root):
    # Remove all widgets from the current page and show the Home page
    for widget in root.winfo_children():
        widget.grid_forget()
    show_home_page(root)

def switch_to_lora_page(root):
    # Remove all widgets from the current page and show the Lora page
    for widget in root.winfo_children():
        widget.grid_forget()
    gui.create_gui(root)

if __name__ == "__main__":
    create_main_gui()
