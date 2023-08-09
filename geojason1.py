# Necessary imports
import numpy as np
import json
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Generate Mock JSON Data
json_data = json.dumps([
    {"Receiver_ID": "Receiver_1", "Timestamp": "2023-08-08 10:00:00", "RSSI": -55},  # Delhi
    {"Receiver_ID": "Receiver_2", "Timestamp": "2023-08-08 10:00:01", "RSSI": -60},  # Mumbai
    {"Receiver_ID": "Receiver_3", "Timestamp": "2023-08-08 10:00:01", "RSSI": -58},  # Kolkata
])

# Parse the JSON data back into a Python list of dictionaries
data = json.loads(json_data)

# Calculate Distances from RSSI
def rssi_to_distance(rssi, p_ref=-50, pl_exp=3.0):
    return 10 ** ((p_ref - rssi) / (10 * pl_exp))

for entry in data:
    entry["Distance"] = rssi_to_distance(entry["RSSI"])

# Triangulate the Position using mock geographical locations in India
coords = {
    "Receiver_1": (0, 10),   # Delhi (North)
    "Receiver_2": (-7, 0),  # Mumbai (West)
    "Receiver_3": (7, 0),   # Kolkata (East)
}

def error(point, coords, distances):
    total_error = 0
    x, y = point
    for receiver, coord in coords.items():
        computed_distance = ((x - coord[0])**2 + (y - coord[1])**2)**0.5
        total_error += (computed_distance - distances[receiver])**2
    return total_error

distances = {entry["Receiver_ID"]: entry["Distance"] for entry in data}
initial_guess = (0, 5)
result = minimize(error, initial_guess, args=(coords, distances))
transmitter_coords = result.x

# Visualization using matplotlib
fig, ax = plt.subplots()
for receiver, coord in coords.items():
    circle = plt.Circle(coord, distances[receiver], fill=False, linestyle='dashed')
    ax.add_artist(circle)
    plt.scatter(*coord, label=f'{receiver} ({coord[0]}, {coord[1]})')

plt.scatter(*transmitter_coords, color='red', marker='x', label=f'Transmitter Estimated ({transmitter_coords[0]:.2f}, {transmitter_coords[1]:.2f})')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Trilateration of Transmitter')
plt.grid(True)
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout()
plt.show()


