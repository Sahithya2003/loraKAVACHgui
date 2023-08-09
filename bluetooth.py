import tkinter as tk
import subprocess
import sys
from PIL import Image, ImageTk

def on_Bluetooth_button_click():
    print("Bluetooth button clicked")
    # Open home.py using subprocess
    python_executable = sys.executable  # Get the path of the current Python interpreter
    subprocess.Popen([python_executable, "home.py"])
    # Close the current window
    root.destroy()

def center_window(w, h):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (w // 2)
    y = (screen_height // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

root = tk.Tk()
root.title("Bluetooth Button")

# Set the background color to #0D0D15
root.config(bg="#0D0D15")

# Adjust the window size using subsample
window_width, window_height = 800, 600
center_window(window_width, window_height)

# Add a small heading above the main heading
small_heading_label = tk.Label(root, text="Bluetooth Communication", font=("Helvetica", 21,"bold"), fg="white", bg="#0D0D15")
small_heading_label.pack(pady=60)

title_label = tk.Label(root, text="This Section is Under Construction", font=("Helvetica", 42, "bold"), fg="#FF867E", bg="#0D0D15", wraplength=700)
title_label.pack(pady=60)

# Load the image for the button and set specific image height and width
image = Image.open('wireless.png')
image = image.resize((209,82 ), Image.ANTIALIAS)
button_image_resized = ImageTk.PhotoImage(image)


# Create a rounded button with the image and set specific button height and width
button_height = 80  # Set the desired button height
button_width = 207   # Set the desired button width
Bluetooth_button = tk.Button(root, image=button_image_resized, command=on_Bluetooth_button_click, bg="#0D0D15", bd=0, height=button_height, width=button_width, borderwidth=0, relief="flat",highlightthickness=0)
Bluetooth_button.pack()

root.mainloop()
