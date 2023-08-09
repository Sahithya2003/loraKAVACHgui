import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import themes

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
    root.title("LoRa")
    theme = themes.dark_theme

    root.config(bg="#0D0D15")

    # Heading
    heading_label = tk.Label(root, text="Wireless Signal Forensics Framework", font=("Helvetica", 42, "bold"), fg="white",
                             bg="#0D0D15", wraplength=window_width, justify=tk.LEFT)
    heading_label.grid(row=0, column=0, columnspan=3, pady=(100, 100), padx=20, sticky="w")

    def go_to_lora_page():
        root.destroy()
        import lorahome
        lorahome.create_gui()

    def go_to_wireless_page():
        root.destroy()
        import wireless
        wireless.create_gui()

    def go_to_bluetooth_page():
        root.destroy()
        import bluetooth
        bluetooth.create_gui()

    rounded_style = ttk.Style()
    rounded_style.configure("Rounded.TButton", background="#0D0D15", borderwidth=0, highlightthickness=0, relief="flat",
                            focuscolor="#0D0D15")
    lora_icon = Image.open("home_Lora.png")  # Replace with your actual image path
    lora_icon = lora_icon.resize((202, 130))
    lora_photo = ImageTk.PhotoImage(lora_icon)

    wireless_icon = Image.open("home_wireless.png")  # Replace with your actual image path
    wireless_icon = wireless_icon.resize((202, 130))
    wireless_photo = ImageTk.PhotoImage(wireless_icon)

    bluetooth_icon = Image.open("home_bluetooth.png")  # Replace with your actual image path
    bluetooth_icon = bluetooth_icon.resize((202, 130))
    bluetooth_photo = ImageTk.PhotoImage(bluetooth_icon)

    button_lora = tk.Button(root, command=go_to_lora_page, bg="#0D0D15",image=lora_photo, highlightthickness=0, bd=0, width=200, height=128)
    button_lora.grid(row=3, column=0, pady=(0, 10))

    button_wireless = tk.Button(root, command=go_to_wireless_page,bg="#0D0D15", image=wireless_photo, highlightthickness=0, bd=0, width=200, height=128)
    button_wireless.grid(row=3, column=1, pady=(0, 10), padx=10)

    button_bluetooth = tk.Button(root, command=go_to_bluetooth_page, bg="#0D0D15",image=bluetooth_photo, highlightthickness=0, bd=0, width=200, height=128)
    button_bluetooth.grid(row=3, column=2, pady=(0, 10))

    # Configure column weights for proper spacing
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    center_window(root)

    root.mainloop()

show_home_page()
