import os
import sys
import tkinter as tk
import subprocess
import sounddevice as sd
import numpy as np
import themes
from PIL import Image, ImageTk

def start_scanning():
    lora_status.set("Scanning...")
    root.update()
    root.after(1000, start_scanning_subprocess)

def start_scanning_subprocess():
    process = subprocess.Popen(
        "python3 test.py",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    update_lora_status(process)

def restart_scanning():
    os.execv(sys.executable, ['python'] + sys.argv)

def update_lora_status(process):
    line = process.stdout.readline().strip()
    if line:
        if '1' in line:
            lora_status.set(' Unauthorized LoRa Detected')
            send_buzzer_signal(1)
        else:
            lora_status.set('Unauthorized LoRa Not Detected')
            send_buzzer_signal(0)

    root.after(200, update_lora_status, process)

def send_buzzer_signal(signal):
    if signal == 1:
        frequency = 1000
        duration = 2
        t = np.linspace(0, duration, int(44100 * duration), False)
        signal_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
        sd.play(signal_wave, 44100)
        sd.wait()

root = tk.Tk()
theme = themes.dark_theme
root.config(bg='#0D0D15')
root.title("Detection")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 800
window_height = 600
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

heading_label = tk.Label(root, text="LoRa Detection Output", font=("Helvetica", 21, "bold"), bg="#0D0D15", fg=theme["fg"])
heading_label.pack(pady=(60))

image = tk.PhotoImage(file="outputwifi.png")
image_label = tk.Label(root, image=image, bg="#0D0D15", width=400, height=200)
image_label.pack()

lora_status = tk.StringVar()

def set_status_and_restart():
    lora_status.set('Scanning...')
    root.update()
    restart_scanning()

lora_label = tk.Label(root, textvariable=lora_status, font=("Helvetica", 37, "bold"), fg="#FF867E", bg="#0D0D15")
lora_label.pack(pady=(20,60))

image2 = Image.open('outputbutton.png')
image2 = image2.resize((209,82 ), Image.ANTIALIAS)
button_image_resized = ImageTk.PhotoImage(image2)


# Create a rounded button with the image and set specific button height and width
button_height = 80  # Set the desired button height
button_width = 207   # Set the desired button width
restart_button = tk.Button(root, image=button_image_resized, command=restart_scanning, bg="#0D0D15", bd=0, height=button_height, width=button_width, borderwidth=0, relief="flat",highlightthickness=0)
restart_button.pack()
restart_button.pack()

start_scanning()

root.mainloop()
