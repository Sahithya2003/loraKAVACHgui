import tkinter as tk
from tkinter import filedialog
import folium
import numpy as np
from scipy.optimize import fsolve

# Mock receiver coordinates around New Delhi
coords = {
    "Receiver_1": (28.7031, 77.1487),  
    "Receiver_2": (28.5024, 77.2874),  
    "Receiver_3": (28.5900, 77.0489)   
}

# Define a single mock transmitter
mock_transmitter = {"Transmitter_1": (28.6139, 77.2090)}

TX_POWER = -40  # dBm, an arbitrary chosen transmitted power
n = 2  # Path loss exponent
RSSI_NOISE = 3  # Adding some noise to the RSSI readings (in dBm)

def calculate_distance_from_rssi(rssi, tx_power, n):
    return 10 ** ((tx_power - rssi) / (10 * n))

def equations(vars, coords, distances):
    x, y = vars
    eq1 = np.sqrt((x - coords["Receiver_1"][0])**2 + (y - coords["Receiver_1"][1])**2) - distances["Receiver_1"]
    eq2 = np.sqrt((x - coords["Receiver_2"][0])**2 + (y - coords["Receiver_2"][1])**2) - distances["Receiver_2"]
    return [eq1, eq2]

# Calculate mock RSSI values with added noise
rssi_values = {
    key: TX_POWER - 10 * n * np.log10(np.sqrt((list(mock_transmitter.values())[0][0]-coord[0])**2 + (list(mock_transmitter.values())[0][1]-coord[1])**2)) + np.random.normal(0, RSSI_NOISE) for key, coord in coords.items()}

# Convert RSSI values to distances
distances = {key: calculate_distance_from_rssi(rssi, TX_POWER, n) for key, rssi in rssi_values.items()}

estimated_x, estimated_y = fsolve(equations, (28.6, 77.2), args=(coords, distances))
estimated_transmitter = {"Estimated_Transmitter": (estimated_x, estimated_y)}

m = folium.Map(location=list(mock_transmitter.values())[0], zoom_start=12)

# Add receiver locations to map
for name, coord in coords.items():
    folium.Marker(coord, tooltip=name).add_to(m)

# Add the mock transmitter for visualization
for name, coord in mock_transmitter.items():
    folium.Marker(coord, tooltip=name, icon=folium.Icon(color="blue")).add_to(m)

# Add the estimated transmitter location
for name, coord in estimated_transmitter.items():
    folium.Marker(coord, tooltip=name, icon=folium.Icon(color="green")).add_to(m)

class GeoMapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoMap GUI")

        self.file_path = None

        self.create_widgets()

    def create_widgets(self):
        self.load_button = tk.Button(self.root, text="Load and Generate Map", command=self.load_and_generate)
        self.load_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="Save Map", command=self.save_map)
        self.save_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=10)

    def load_and_generate(self):
        # Your existing code for loading and generating the map
        # ... (Replace with your code that creates and displays the map)

    def save_map(self):
        if self.file_path:
            m.save(self.file_path)
            print(f"Map saved as {self.file_path}")
        else:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML Files", "*.html")])
            if self.file_path:
                m.save(self.file_path)
                print(f"Map saved as {self.file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeoMapGUI(root)
    root.mainloop()
