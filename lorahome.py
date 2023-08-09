import tkinter as tk
from tkinter import ttk
import themes
from PIL import Image, ImageTk
import subprocess
import sys

def create_gui():
    root = tk.Tk()
    root.title("LoRa")
    theme = themes.dark_theme
    root.config(bg="#0D0D15")

    window_width = 800
    window_height = 600

    def center_window(window):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    center_window(root)  # Center the window on startup

    def go_to_gui_page():
        root.destroy()
        import gui
        gui.create_gui()
    def go_to_gui2_page():
        root.destroy()
        import gui2
        gui2.create_gui()

    def go_to_geohome():
        root.destroy()
        import geo_home
        geo_home.create_gui()
    def go_to_freq():
        root.destroy()
        import freq
        freq.create_gui()
    def go_to_gui_page():
        root.destroy()
        from gui import run
        run()
    def on_Bluetooth_button_click():
     print("back button clicked")
     # Open home.py using subprocess
     python_executable = sys.executable  # Get the path of the current Python interpreter
     subprocess.Popen([python_executable, "home.py"])
     # Close the current window
     root.destroy()

    root.resizable(False, False)  # Disable window resizing

    title_label = tk.Label(root, text="LoRa Forensics", font=("Helvetica", 24, "bold"), bg="#0D0D15", fg="white")
    title_label.pack(fill="none", pady=20)

    button_frame = tk.Frame(root, bg="#0D0D15")
    button_frame.pack(fill="none", expand=True, padx=20, pady=20)

    images = []
    button_commands = [go_to_gui_page, go_to_freq,go_to_gui2_page, go_to_geohome]
    image = Image.open('wireless.png')
    image = image.resize((209,82 ), Image.ANTIALIAS)
    button_image_resized = ImageTk.PhotoImage(image)


     # Create a rounded button with the image and set specific button height and width
    button_height = 80  # Set the desired button height
    button_width = 207   # Set the desired button width
    Bluetooth_button = tk.Button(root, image=button_image_resized, command=on_Bluetooth_button_click, bg="#0D0D15", bd=0, height=button_height, width=button_width, borderwidth=0, relief="flat",highlightthickness=0)
    Bluetooth_button.pack()
    for i in range(2):
        row_images = []
        for j in range(2):
            # Modify this based on your image filenames
            image_path = f"button{i + 1}{j + 1}.png"
            img = Image.open(image_path)
            img = ImageTk.PhotoImage(img)

            button = ttk.Button(button_frame, image=img, command=button_commands[i * 2 + j])
            button.image = img  # Store a reference to the image to prevent garbage collection
            button.grid(row=i, column=j, padx=20, pady=20)
            row_images.append(button)
            button_frame.grid_columnconfigure(j, weight=1)
            button_frame.grid_rowconfigure(i, weight=1)
        images.append(row_images)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
