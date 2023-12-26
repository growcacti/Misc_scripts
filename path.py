import tkinter as tk
from tkinter import filedialog

def browse_source():
    source_path = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_path)

def browse_destination():
    destination_path = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, destination_path)

# Create the main window
root = tk.Tk()
root.title("Path Selector")

# Create labels and Entry widgets for source and destination paths
source_label = tk.Label(root, text="Source Path:")
source_label.pack()
source_entry = tk.Entry(root, width=40)
source_entry.pack()
destination_label = tk.Label(root, text="Destination Path:")
destination_label.pack()
destination_entry = tk.Entry(root, width=40)
destination_entry.pack()

# Create buttons to open file dialogs
source_button = tk.Button(root, text="Browse Source", command=browse_source)
source_button.pack()
destination_button = tk.Button(root, text="Browse Destination", command=browse_destination)
destination_button.pack()

# Run the Tkinter main loop
root.mainloop()
