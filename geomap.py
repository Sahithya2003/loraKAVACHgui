import tkinter as tk
from tkinter import filedialog
import folium
import numpy as np
from scipy.optimize import fsolve
import webbrowser
import os
from PIL import Image, ImageTk
from themes import dark_theme, light_theme


class GeoMapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoMap Generator")
        

        self.root.config(bg="#0D0D15")

        # Prevent window from being resizable
        self.root.resizable(False, False)

        # Create the GUI widgets as before...

        # Calculate the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the window width and height
        window_width = 800  # Adjust as needed
        window_height = 600  # Adjust as needed

        # Calculate the position to center the window on the screen
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set the window geometry to center the GUI
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.heading_label = tk.Label(self.root, text="Geo Scanner", font=("Helvetica", 37,"bold"), bg="#0D0D15", fg="white")
        self.heading_label.pack(pady=(60,40))  # Add some padding on top
        self.coords_base_text = '''\
Receiver_1: 28.7031, 77.1487
Receiver_2: 28.5024, 77.2874
Receiver_3: 28.5900, 77.0489
'''

        self.coords_entry = tk.Text(self.root, height=5, width=30, bg="#fff", fg="black", font="Helvetica")
        self.coords_entry.insert(tk.END, self.coords_base_text)
        self.coords_entry.pack(pady=(30))
        self.transmitter_entry = tk.Entry(
            self.root, bg="#fff", fg="black", font="Helvetica")
        self.transmitter_entry.insert(0, "28.6139, 77.2090")
        self.transmitter_entry.pack()

        self.tx_power_entry = tk.Entry(
            self.root, bg="#fff", fg="black", font="Helvetica")
        self.tx_power_entry.insert(0, "-40")
        self.tx_power_entry.pack()

        self.n_entry = tk.Entry(
            self.root, bg="#fff", fg="black", font="Helvetica")
        self.n_entry.insert(0, "2")
        self.n_entry.pack()

        self.rssi_noise_entry = tk.Entry(
            self.root, bg="#fff", fg="black", font="Helvetica")
        self.rssi_noise_entry.insert(0, "3")
        self.rssi_noise_entry.pack(pady=(0,30))
        generate_image = Image.open("GenerateMap.png")  # Replace with your image path
        save_image = Image.open("SaveMap.png")  # Replace with your image path

        # Resize the images if needed
        generate_image = generate_image.resize((156,48), Image.ANTIALIAS)
        save_image = save_image.resize((156,48), Image.ANTIALIAS)

        # Create PhotoImage objects
        self.generate_photo = ImageTk.PhotoImage(generate_image)
        self.save_photo = ImageTk.PhotoImage(save_image)

        # Create the "Generate Map" button with the image
        self.generate_button = tk.Button(
            self.root, image=self.generate_photo, command=self.generate_map, bg="#0D0D15",highlightthickness=0, borderwidth=0)
        self.generate_button.pack(pady=10)

        # Create the "Save Map" button with the image
        self.save_button = tk.Button(
            self.root, image=self.save_photo, command=self.save_map, bg="#0D0D15",highlightthickness=0, borderwidth=0)
        self.save_button.pack(pady=5)


        # self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit,
        #                              bg=self.theme["home_bg"],  font="Helvetica")
        # self.quit_button.pack(pady=10)

    def parse_coordinates(self, text):
        coords = {}
        lines = text.split('\n')
        for line in lines:
            if ':' in line:
                name, coord = line.split(':')
                lat, lon = map(float, coord.strip().split(','))
                coords[name.strip()] = (lat, lon)
        return coords

    def generate_map(self):
        coords_text = self.coords_entry.get("1.0", tk.END).strip()
        mock_transmitter = {"Transmitter_1": tuple(
            map(float, self.transmitter_entry.get().split(',')))}
        tx_power = float(self.tx_power_entry.get())
        n = float(self.n_entry.get())
        rssi_noise = float(self.rssi_noise_entry.get())

        coords = self.parse_coordinates(coords_text)

        # Calculate mock RSSI values with added noise
        rssi_values = {
            key: tx_power - 10 * n * np.log10(np.sqrt((list(mock_transmitter.values())[0][0]-coord[0])**2 + (list(mock_transmitter.values())[0][1]-coord[1])**2)) + np.random.normal(0, rssi_noise) for key, coord in coords.items()}

        # Convert RSSI values to distances
        distances = {key: self.calculate_distance_from_rssi(
            rssi, tx_power, n) for key, rssi in rssi_values.items()}

        estimated_x, estimated_y = self.fsolve_equations(
            (28.6, 77.2), coords, distances)
        estimated_transmitter = {
            "Estimated_Transmitter": (estimated_x, estimated_y)}

        # Create the folium map
        m = folium.Map(location=list(
            mock_transmitter.values())[0], zoom_start=12)

        # Add receiver locations to map
        for name, coord in coords.items():
            folium.Marker(coord, tooltip=name).add_to(m)

        # Add the mock transmitter for visualization
        for name, coord in mock_transmitter.items():
            folium.Marker(coord, tooltip=name,
                          icon=folium.Icon(color="blue")).add_to(m)

        # Add the estimated transmitter location
        for name, coord in estimated_transmitter.items():
            folium.Marker(coord, tooltip=name,
                          icon=folium.Icon(color="green")).add_to(m)

        # Save the map as HTML
        map_file_path = "generated_map.html"
        m.save(map_file_path)

        # Open the generated map in the default web browser
        webbrowser.open(os.path.abspath(map_file_path))

    def calculate_distance_from_rssi(self, rssi, tx_power, n):
        return 10 ** ((tx_power - rssi) / (10 * n))

    def fsolve_equations(self, initial_guess, coords, distances):
        return fsolve(self.equations, initial_guess, args=(coords, distances))

    def equations(self, vars, coords, distances):
        x, y = vars
        eq1 = np.sqrt((x - coords["Receiver_1"][0])**2 + (y -
                      coords["Receiver_1"][1])**2) - distances["Receiver_1"]
        eq2 = np.sqrt((x - coords["Receiver_2"][0])**2 + (y -
                      coords["Receiver_2"][1])**2) - distances["Receiver_2"]
        return [eq1, eq2]

    def save_map(self):
        if hasattr(self, 'map'):
            file_path = filedialog.asksaveasfilename(
                defaultextension=".html", filetypes=[("HTML Files", "*.html")])
            if file_path:
                self.map.save(file_path)
                print(f"Map saved as {file_path}")
        else:
            print("No map to save.")


def create_gui():
    root = tk.Tk()
    app = GeoMapGUI(root)
    root.mainloop()
if __name__ == "__main__":
    create_gui()
