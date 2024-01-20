import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
import skrf as rf


def plot_from_csv(file_path):
    """
    Reads a CSV file and plots a graph based on its contents.
    """
    # Read the CSV file using Pandas
    data = pd.read_csv(file_path)

    # Assuming the CSV has two columns 'x' and 'y'
    x = data['x']
    y = data['y']

    # Plotting the graph
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o')
    plt.title('Graph from CSV Data')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.show()



def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title='Select a S2P file', filetypes=[('S2P files', '*.s2p'),("All Files", "*.*")])
                                           
    if file_path:
        phase_data, frequencies = read_s2p(file_path)
        plot_phase(phase_data, frequencies)

if __name__ == "__main__":
    select_file()
