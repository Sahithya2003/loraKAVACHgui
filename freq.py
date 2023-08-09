import tkinter as tk
from tkinter import scrolledtext
import os

def create_gui():
    root = tk.Tk()
    root.title("Frequency Data Viewer")
    root.geometry("800x600")

    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    text_widget.pack(padx=20, pady=20)

    def load_text_file():
        text_file_path = "frequecy.txt"  # Replace with the actual path to your text file
        if os.path.exists(text_file_path):
            with open(text_file_path, "r") as file:
                content = file.read()
                text_widget.delete("1.0", tk.END)  # Clear existing text
                text_widget.insert(tk.END, content)
        else:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, "Frequency data file not found.")

    load_button = tk.Button(root, text="Load Frequency Data", command=load_text_file)
    load_button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
