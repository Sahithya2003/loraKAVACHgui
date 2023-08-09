import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import json
from scipy.optimize import minimize
import matplotlib.pyplot as plt

class TrilaterationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trilateration Visualization")

        self.data = None
        self.coords = {}
        self.distances = None
        self.transmitter_coords = None

        self.json_input_frame = ttk.Frame(self.root)
        self.json_input_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        ttk.Label(self.json_input_frame, text="JSON Data").grid(row=0, columnspan=3)

        self.json_data_text = scrolledtext.ScrolledText(self.json_input_frame, height=10, width=50)
        self.json_data_text.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.load_json_button = ttk.Button(self.json_input_frame, text="Load JSON", command=self.load_json)
        self.load_json_button.grid(row=2, column=0, padx=5, pady=5)

        self.save_json_button = ttk.Button(self.json_input_frame, text="Save JSON", command=self.save_json)
        self.save_json_button.grid(row=2, column=1, padx=5, pady=5)

        self.receiver_input_frame = ttk.Frame(self.root)
        self.receiver_input_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        ttk.Label(self.receiver_input_frame, text="Receiver Coordinates").grid(row=0, columnspan=2)

        self.receiver_entries = {}
        for idx, receiver in enumerate(["Receiver_1", "Receiver_2", "Receiver_3"]):
            ttk.Label(self.receiver_input_frame, text=receiver).grid(row=idx+1, column=0, padx=5, pady=5)
            entry = ttk.Entry(self.receiver_input_frame)
            entry.grid(row=idx+1, column=1, padx=5, pady=5)
            self.receiver_entries[receiver] = entry

        self.calculate_button = ttk.Button(root, text="Calculate", command=self.calculate_transmitter_coords)
        self.calculate_button.grid(row=2, column=0, padx=10, pady=10)

        self.plot_button = ttk.Button(root, text="Plot", command=self.plot)
        self.plot_button.grid(row=2, column=1, padx=10, pady=10)

    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "r") as json_file:
                json_data = json_file.read()
                self.json_data_text.delete("1.0", tk.END)
                self.json_data_text.insert("1.0", json_data)

    def save_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            json_data = self.json_data_text.get("1.0", "end-1c")
            with open(file_path, "w") as json_file:
                json_file.write(json_data)

    def calculate_transmitter_coords(self):
        json_data = self.json_data_text.get("1.0", "end-1c")
        self.data = json.loads(json_data)
        self.coords = {receiver: self.parse_coordinates(entry.get()) for receiver, entry in self.receiver_entries.items()}
        self.distances = {entry["Receiver_ID"]: entry["Distance"] for entry in self.data}
        initial_guess = (0, 5)
        result = minimize(self.error, initial_guess, args=(self.coords, self.distances))
        self.transmitter_coords = result.x

    def parse_coordinates(self, text):
        try:
            x, y = map(float, text.split(","))
            return x, y
        except ValueError:
            return (0, 0)

    def error(self, point, coords, distances):
        total_error = 0
        x, y = point
        for receiver, coord in coords.items():
            computed_distance = ((x - coord[0])**2 + (y - coord[1])**2)**0.5
            total_error += (computed_distance - distances[receiver])**2
        return total_error

    def plot(self):
        if self.transmitter_coords is None:
            tk.messagebox.showerror("Error", "Please calculate first.")
            return

        fig, ax = plt.subplots()
        for receiver, coord in self.coords.items():
            circle = plt.Circle(coord, self.distances[receiver], fill=False, linestyle='dashed')
            ax.add_artist(circle)
            plt.scatter(*coord, label=f'{receiver} ({coord[0]}, {coord[1]})')

        plt.scatter(*self.transmitter_coords, color='red', marker='x', label=f'Transmitter Estimated ({self.transmitter_coords[0]:.2f}, {self.transmitter_coords[1]:.2f})')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Trilateration of Transmitter')
        plt.grid(True)
        plt.legend()
        plt.gca().set_aspect('equal', adjustable='box')

        # Display plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().grid(row=4, columnspan=2, padx=10, pady=10)

def create_gui():
    root = tk.Tk()
    app = TrilaterationApp(root)
    root.mainloop()
if __name__ == "__main__":
    create_gui()
