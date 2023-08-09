import tkinter as tk
from tkinter import filedialog
import subprocess
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import scipy.io as sio

output_file_entry = None  
freq_entry = None
rate_entry = None
duration_entry = None
channels_entry = None
gain_entry = None
mat_output_var = None
ax = None
canvas = None

def browse_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".mat", filetypes=[("MATLAB files", "*.mat")])
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
    ax.plot(range(length), samps, color='green')  # Set plot color to green
    ax.set_xlabel('Sample Index', color='#1DFF00')
    ax.set_ylabel('Amplitude', color='#1DFF00')
    ax.set_title('Plot of ' + filename, color='#1DFF00')
    ax.grid(True)
    ax.set_facecolor('#263238')  # Set the plot background color to dark theme
    ax.tick_params(axis='x', colors='#1DFF00')
    ax.tick_params(axis='y', colors='#1DFF00')
    ax.spines['bottom'].set_color('#1DFF00')
    ax.spines['top'].set_color('#1DFF00')
    ax.spines['left'].set_color('#1DFF00')
    ax.spines['right'].set_color('#1DFF00')
    canvas.draw()


def create_g():
    global output_file_entry, mat_output_var, ax, canvas

    root = tk.Tk()
    root.title("USRP Data Receiver GUI")
    root.config(bg="#263238")  # Apply dark theme background color

    # Create a PanedWindow
    paned_window = tk.PanedWindow(orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Create left frame for inputs
    left_frame = tk.Frame(paned_window, bg="#263238", highlightthickness=0)  # Apply dark theme background color and remove border
    paned_window.add(left_frame)

    # Labels
    tk.Label(left_frame, text="Output File:", bg="#263238", fg="#1DFF00").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    tk.Label(left_frame, text="Center Frequency (Hz):", bg="#263238", fg="#1DFF00").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    tk.Label(left_frame, text="Sample Rate (Hz):", bg="#263238", fg="#1DFF00").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    tk.Label(left_frame, text="Duration (seconds):", bg="#263238", fg="#1DFF00").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    tk.Label(left_frame, text="Channels (space-separated):", bg="#263238", fg="#1DFF00").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    tk.Label(left_frame, text="Gain (dB):", bg="#263238", fg="#1DFF00").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)

    # Entries
    output_file_entry = tk.Entry(left_frame, bg="#fff", fg="#263238")  # Apply dark theme background and foreground colors
    freq_entry = tk.Entry(left_frame, bg="#fff", fg="#263238")
    rate_entry = tk.Entry(left_frame, bg="#fff", fg="#263238")
    duration_entry = tk.Entry(left_frame, bg="#fff", fg="#263238")
    channels_entry = tk.Entry(left_frame, bg="#fff", fg="#263238")
    gain_entry = tk.Entry(left_frame, bg="#fff", fg="#263238")

    output_file_entry.grid(row=0, column=1, padx=5, pady=5)
    freq_entry.grid(row=1, column=1, padx=5, pady=5)
    rate_entry.grid(row=2, column=1, padx=5, pady=5)
    duration_entry.grid(row=3, column=1, padx=5, pady=5)
    channels_entry.grid(row=4, column=1, padx=5, pady=5)
    gain_entry.grid(row=5, column=1, padx=5, pady=5)
    

    # Buttons
    tk.Button(left_frame, text="Browse", command=browse_output_file, bg="#1DFF00", fg="#263238", highlightthickness=0).grid(row=0, column=2, padx=5, pady=5)  # Remove border
    tk.Button(left_frame, text="Run and Plot", command=run_script_and_plot, bg="#1DFF00", fg="#263238", highlightthickness=0).grid(row=6, column=0, columnspan=3, padx=5, pady=5)  # Remove border
    tk.Button(left_frame, text="Browse Plot File", command=browse_plot_file, bg="#1DFF00", fg="#263238", highlightthickness=0).grid(row=7, column=0, columnspan=3, padx=5, pady=5)  # Remove border

    # Checkboxes
    mat_output_var = tk.BooleanVar()
    tk.Checkbutton(left_frame, text="Save in MATLAB .mat format", variable=mat_output_var, bg="#263238", fg="#1DFF00", highlightthickness=0).grid(row=8, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)  # Remove border

    # Create right frame for graph
    right_frame = tk.Frame(paned_window, bg="#263238", highlightthickness=0)  # Apply dark theme background color and remove border
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
    create_g()
