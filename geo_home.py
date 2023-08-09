import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import themes
import subprocess
import sys

window_width = 800
window_height = 600

def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

def show_home_page():
    root = tk.Tk()
    root.title("geotime")
    theme = themes.dark_theme

    root.config(bg="#0D0D15")
    root.resizable(False, False)  # Disable window resizing


    # Heading
    heading_label = tk.Label(root, text="Geo Location Tracking", font=("Helvetica", 42, "bold"), fg="white",
                             bg="#0D0D15", wraplength=window_width, justify=tk.LEFT)
    heading_label.grid(row=0, column=0, columnspan=3, pady=(100, 100), padx=20, sticky="w")

    def go_to_geotime_page():
        root.destroy()
        import geotime
        geotime.create_gui()

    def go_to_geojason1_page():
        root.destroy()
        import geojason1
        geojason1.create_gui()

    def go_to_geomap_page():
        root.destroy()
        import geomap
        geomap.create_gui()
    def on_Bluetooth_button_click():
     print("back button clicked")
     # Open home.py using subprocess
     python_executable = sys.executable  # Get the path of the current Python interpreter
     subprocess.Popen([python_executable, "home.py"])
     # Close the current window
     root.destroy()
    
    rounded_style = ttk.Style()
    rounded_style.configure("Rounded.TButton", background="#0D0D15", borderwidth=0, highlightthickness=0, relief="flat",
                            focuscolor="#0D0D15")
    geotime_icon = Image.open("Timescan.png")  # Replace with your actual image path
    geotime_icon = geotime_icon.resize((202, 130))
    geotime_photo = ImageTk.PhotoImage(geotime_icon)

    geojason_icon = Image.open("JSONscan.png")  # Replace with your actual image path
    geojason_icon = geojason_icon.resize((202, 130))
    geojason_photo = ImageTk.PhotoImage(geojason_icon)

    geomap_icon = Image.open("Geomap.png")  # Replace with your actual image path
    geomap_icon = geomap_icon.resize((202, 130))
    geomap_photo = ImageTk.PhotoImage(geomap_icon)

    button_geotime = tk.Button(root, command=go_to_geotime_page, bg="#0D0D15",image=geotime_photo, highlightthickness=0, bd=0, width=200, height=128)
    button_geotime.grid(row=3, column=0, pady=(0, 10))

    button_geojason = tk.Button(root, command=go_to_geojason1_page,bg="#0D0D15", image=geojason_photo, highlightthickness=0, bd=0, width=200, height=128)
    button_geojason.grid(row=3, column=1, pady=(0, 10), padx=10)

    button_geomap = tk.Button(root, command=go_to_geomap_page, bg="#0D0D15",image=geomap_photo, highlightthickness=0, bd=0, width=200, height=128)
    button_geomap.grid(row=3, column=2, pady=(0, 10))
    # image = Image.open('wireless.png')
    # image = image.resize((209,82 ), Image.ANTIALIAS)
    # button_image_resized = ImageTk.PhotoImage(image)
    # button_height = 80  # Set the desired button height
    # button_width = 207   # Set the desired button width
    # Bluetooth_button = tk.Button(root, image=button_image_resized, command=on_Bluetooth_button_click, bg="#0D0D15", bd=0, height=button_height, width=button_width, borderwidth=0, relief="flat",highlightthickness=0)
    # Bluetooth_button.grid(row=9, column=1, pady=(0, 10))
    
    # Configure column weights for proper spacing
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
   


     # Create a rounded button with the image and set specific button height and width
    

    center_window(root)

    root.mainloop()

show_home_page()
