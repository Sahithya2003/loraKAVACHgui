import tkinter as tk
from tkinter import filedialog
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import scipy.io as sio
import themes
from PIL import Image, ImageTk

output_file_entry = None
freq_entry = None
rate_entry = None
duration_entry = None
channels_entry = None
gain_entry = None
mat_output_var = None
ax = None
canvas = None
root = None


def browse_output_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".mat", filetypes=[("MATLAB files", "*.mat")])
    if file_path:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, file_path)


def run_script_and_plot():
    command = f"/bin/python3 /home/zero_two/USRP/final_manual_arguments.py -o \"{output_file_entry.get()}\" -f {freq_entry.get()} -r {rate_entry.get()} -d {duration_entry.get()} -c {channels_entry.get()} -g {gain_entry.get()}"
    if mat_output_var.get():
        command += " -m"

    subprocess.run(command, shell=True)

    # Plot the data after running the script
    plot_mat_file(output_file_entry.get())


def browse_plot_file():
    file_path = filedialog.askopenfilename(filetypes=[("MATLAB files", "*.mat")])
    if file_path:
        plot_mat_file(file_path)


def plot_mat_file(filename):
    global ax, canvas
    data = sio.loadmat(filename, squeeze_me=True)
    samps = data['samps']
    length = len(samps)

    # Clear previous plot (if any)
    ax.clear()
    ax.plot(range(length), samps)
    ax.set_xlabel('Sample Index', color='white')
    ax.set_ylabel('Amplitude', color='white')
    ax.set_title('Plot of ' + filename, color='white')
    ax.grid(True)
    canvas.draw()


def create_gui():
    global output_file_entry, freq_entry, rate_entry, duration_entry, channels_entry, gain_entry, mat_output_var, ax, canvas, root

    root = tk.Tk()
    root.title("USRP Data Receiver GUI")

    # Use the dark_theme or light_theme based on your preference
    theme = themes.light_theme  # You can change this to themes.dark_theme if needed

    # Apply theme colors
    root.config(bg=theme["bg"])

    # Calculate the center position of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 800
    window_height = 600
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    # Set the window position and size
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Create a PanedWindow
    paned_window = tk.PanedWindow(orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Create left frame for inputs
    left_frame = tk.Frame(paned_window, padx=10, pady=10, bg=theme["bg"] )
    paned_window.add(left_frame)

    # Labels with theme colors
    tk.Label(left_frame, text="Output File:", bg=theme["bg"], fg=theme["fg"], font=theme["font"]).grid(row=0, column=0, sticky=tk.W)
    tk.Label(left_frame, text="Center Frequency (Hz):", bg=theme["bg"], fg=theme["fg"], font=theme["font"]).grid(row=1, column=0, sticky=tk.W)
    tk.Label(left_frame, text="Sample Rate (Hz):", bg=theme["bg"], fg=theme["fg"], font=theme["font"]).grid(row=2, column=0, sticky=tk.W)
    tk.Label(left_frame, text="Duration (seconds):", bg=theme["bg"], fg=theme["fg"], font=theme["font"]).grid(row=3, column=0, sticky=tk.W)
    tk.Label(left_frame, text="Channels (space-separated):", bg=theme["bg"], fg=theme["fg"], font=theme["font"]).grid(row=4, column=0, sticky=tk.W)
    tk.Label(left_frame, text="Gain (dB):", bg=theme["bg"], fg=theme["fg"], font=theme["font"]).grid(row=5, column=0, sticky=tk.W)

    # Entries with theme colors
    output_file_entry = tk.Entry(left_frame, bg=theme["entry_bg"], fg=theme["fg"], font=theme["font"])
    freq_entry = tk.Entry(left_frame, bg=theme["entry_bg"], fg=theme["fg"], font=theme["font"])
    rate_entry = tk.Entry(left_frame, bg=theme["entry_bg"], fg=theme["fg"], font=theme["font"])
    duration_entry = tk.Entry(left_frame, bg=theme["entry_bg"], fg=theme["fg"], font=theme["font"])
    channels_entry = tk.Entry(left_frame, bg=theme["entry_bg"], fg=theme["fg"], font=theme["font"])
    gain_entry = tk.Entry(left_frame, bg=theme["entry_bg"], fg=theme["fg"], font=theme["font"])

    output_file_entry.grid(row=0, column=1,sticky='w' )
    freq_entry.grid(row=1, column=1 , pady=10, sticky='w')
    rate_entry.grid(row=2, column=1,  pady=10, sticky='w')
    duration_entry.grid(row=3, column=1, pady=10, sticky='w')
    channels_entry.grid(row=4, column=1, pady=10, sticky='w')
    gain_entry.grid(row=5, column=1, pady=10, sticky='w')

    # Load the images
    button_image = Image.open("button.png")
    button1_image = Image.open("button1.png")
    button2_image = Image.open("button2.png")

    # Resize the images as needed
    button_image = button_image.resize((96, 32), Image.ANTIALIAS)
    button1_image = button1_image.resize((156, 50), Image.ANTIALIAS)
    button2_image = button2_image.resize((156, 50), Image.ANTIALIAS)

    # Convert images to PhotoImage objects
    button_photo = ImageTk.PhotoImage(button_image)
    button1_photo = ImageTk.PhotoImage(button1_image)
    button2_photo = ImageTk.PhotoImage(button2_image)

    # Buttons
    tk.Button(left_frame, image=button_photo, command=browse_output_file, bg=theme["bg"], fg=theme["fg"], bd=0,highlightthickness=0).grid(row=0, column=2,columnspan=1,padx=20,  pady=10, sticky='w')
    tk.Button(left_frame, image=button1_photo, command=run_script_and_plot, bg=theme["bg"], fg=theme["fg"], bd=0,highlightthickness=0).grid(row=6, column=0, columnspan=1, padx=100, pady=50, sticky='w')
    tk.Button(left_frame, image=button2_photo, command=browse_plot_file, bg=theme["bg"], fg=theme["fg"], bd=0,highlightthickness=0).grid(row=6, column=1, columnspan=1, padx=20, pady=50, sticky='w')

    # Checkboxes
    mat_output_var = tk.BooleanVar()
    tk.Checkbutton(left_frame, text="Save in MATLAB .mat format", variable=mat_output_var,
                   bg=theme["bg"], fg=theme["fg"], font=theme["font"],highlightthickness=0).grid(row=9, column=0, columnspan=2, sticky=tk.W)

    # Create right frame for graph
    # Apply dark theme background color
    right_frame = tk.Frame(paned_window,  bg=theme["bg"],)
    paned_window.add(right_frame)

    # Create a matplotlib Figure and add a subplot
    fig = plt.Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()

    # Create a toolbar for the plot
    toolbar = NavigationToolbar2Tk(canvas, right_frame)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
