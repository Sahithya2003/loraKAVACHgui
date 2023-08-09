import tkinter as tk
from tkinter import ttk
import numpy as np
from scipy.optimize import fsolve
from PIL import Image, ImageTk

class GeolocationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geolocation App")
        self.root.config(bg="#0D0D15")
        self.style = ttk.Style()
        self.style.configure("TLabel", foreground="white", background="#0D0D15", font=("Helvetica", 12))
        self.style.configure("TButton", foreground="white", background="#0D0D15")
        self.style.map("TButton",
            foreground=[("active", "white"), ("pressed", "white")],
            background=[("active", "#007acc"), ("pressed", "#005299")]
        )

        self.coords = {}
        self.mock_transmitters = {}

        self.create_input_boxes()

        self.result_label = ttk.Label(root, text="Result:")
        self.result_label.grid(row=9, columnspan=2)
        # Define calculate_button and map_button attributes
        self.calculate_button = None
        self.map_button = None

        self.load_buttons()

    def load_buttons(self):
        self.calculate_button = ttk.Button(self.root, command=self.calculate)
        self.calculate_button.grid(row=8, column=3, padx=20, pady=10, sticky="e")

        self.calculate_img = Image.open("calculate.png").resize((156, 48), Image.ANTIALIAS)
        self.calculate_img = ImageTk.PhotoImage(self.calculate_img)
        self.calculate_button.config(image=self.calculate_img)

        self.map_button = ttk.Button(self.root, command=self.open_map)
        self.map_button.grid(row=8, column=4, padx=20, pady=10, sticky="w")

        self.map_img = Image.open("openmap.png").resize((156, 48), Image.ANTIALIAS)
        self.map_img = ImageTk.PhotoImage(self.map_img)
        self.map_button.config(image=self.map_img)

        app_width = 800
        app_height = 600
        x_position = (self.root.winfo_screenwidth() - app_width) // 2
        y_position = (self.root.winfo_screenheight() - app_height) // 2
        self.root.geometry(f"{app_width}x{app_height}+{x_position}+{y_position}")
    def create_input_boxes(self):
        receiver_label = ttk.Label(self.root, text="Receiver Coordinates", font=("Helvetica", 27, "bold"))
        receiver_label.grid(row=0, column=3, columnspan=3, pady=(100,20))

        for idx, receiver_name in enumerate(["Receiver 1", "Receiver 2", "Receiver 3"], start=1):
            label = ttk.Label(self.root, text=receiver_name)
            label.grid(row=idx, column=2, pady=5)
            lat_entry = ttk.Entry(self.root)
            lat_entry.grid(row=idx, column=3,  pady=5)
            lon_entry = ttk.Entry(self.root)
            lon_entry.grid(row=idx, column=4, pady=5)
            self.coords[receiver_name] = (lat_entry, lon_entry)

        transmitter_label = ttk.Label(self.root, text="Transmitter Coordinates", font=("Helvetica", 27, "bold"))
        transmitter_label.grid(row=4, column=3, columnspan=3, pady=(20,10))

        for idx, transmitter_name in enumerate(["Transmitter 1", "Transmitter 2", "Transmitter 3"], start=5):
            label = ttk.Label(self.root, text=transmitter_name)
            label.grid(row=idx, column=2,  padx=(20, 5), pady=5)
            lat_entry = ttk.Entry(self.root)
            lat_entry.grid(row=idx, column=3, padx=(5, 20), pady=5)
            lon_entry = ttk.Entry(self.root)
            lon_entry.grid(row=idx, column=4, padx=(5, 20), pady=5)
            self.mock_transmitters[transmitter_name] = (lat_entry, lon_entry)

    def calculate(self):
        c = 299792.458  # Speed of light in km/s

        # Extract input values from the entry boxes
        for receiver_name, (lat_entry, lon_entry) in self.coords.items():
            lat, lon = float(lat_entry.get()), float(lon_entry.get())
            self.coords[receiver_name] = (lat, lon)

        for transmitter_name, (lat_entry, lon_entry) in self.mock_transmitters.items():
            lat, lon = float(lat_entry.get()), float(lon_entry.get())
            self.mock_transmitters[transmitter_name] = (lat, lon)

        estimated_transmitters = {}

        for t_name, t_location in self.mock_transmitters.items():
            time_delays = {key: np.sqrt((t_location[0]-coord[0])**2 + (t_location[1]-coord[1])**2) / c for key, coord in self.coords.items()}
            relative_timestamps = {key: val - time_delays["Receiver 1"] for key, val in time_delays.items()}

            estimated_x, estimated_y = fsolve(self.equations, (28.6, 77.2), args=(self.coords, c, relative_timestamps))
            estimated_transmitters[t_name] = (estimated_x, estimated_y)

        self.result_label.config(text="Calculation completed.")

    def equations(self, vars, coords, c, relative_timestamps):
        x, y = vars
        eq1 = np.sqrt((x - coords["Receiver 1"][0])**2 + (y - coords["Receiver 1"][1])**2) - np.sqrt((x - coords["Receiver 2"][0])**2 + (y - coords["Receiver 2"][1])**2) - c * relative_timestamps["Receiver 2"]
        eq2 = np.sqrt((x - coords["Receiver 1"][0])**2 + (y - coords["Receiver 1"][1])**2) - np.sqrt((x - coords["Receiver 3"][0])**2 + (y - coords["Receiver 3"][1])**2) - c * relative_timestamps["Receiver 3"]
        return [eq1, eq2]

    def open_map(self):
        map_path = "map.html"  # Path to the generated map HTML file
        import webbrowser
        webbrowser.open(map_path)

def create_gui():
    root = tk.Tk()
    app = GeolocationApp(root)
    root.mainloop()
if __name__ == "__main__":
    create_gui()
