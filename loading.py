import tkinter as tk
import math
import subprocess

def show_loading_animation():
    root = tk.Tk()
    root.title("Wireless")
    # root.config(bg="#333")  # Apply dark theme background color
    #Add a background color to the Main Window
    root.config(bg = '#fff000')

 

    # Remove window decorations (box and title bar)
    root.overrideredirect(True)

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the center position
    window_width = 200
    window_height = 200
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set the window position
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Function to switch to the main app (main_app.py)
    def switch_to_main_app():
        root.destroy()  # Close the root window of loading.py
        subprocess.Popen(["python", "main_app.py"])  # Open the main_app.py

    # Function to update the loading circle animation
    def update_loading_circle(angle):
        canvas.delete("all")
        # Draw the "Redantio" text in the middle
        canvas.create_text(100, 100, text="Redantio", font=("Arial", 16), fill="white")
        # Draw the loading circle arc
        canvas.create_arc(10, 10, 190, 190, start=angle, extent=120, width=5, style=tk.ARC, outline="white")
        if angle > 359:
            switch_to_main_app()  # After animation, switch to the main app (main_app.py)
        else:
            root.after(50, update_loading_circle, angle + 10)

    # Create a canvas for drawing the loading circle
    canvas = tk.Canvas(root, width=200, height=200, bg="#333", highlightthickness=0)
    canvas.pack(expand=True)

    # Start the loading circle animation
    update_loading_circle(0)

    root.mainloop()

show_loading_animation()
