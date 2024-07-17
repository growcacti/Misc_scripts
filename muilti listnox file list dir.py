import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import time

class ScrollableListbox:
    def __init__(self, root):
        # Create a frame to contain the Listbox and Scrollbar
        self.frame = ttk.Frame(root)
        self.frame.grid(padx=10, pady=10, sticky=tk.NSEW)

        # Create a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # Create the listbox and attach the scrollbar
        self.listbox = tk.Listbox(self.frame, yscrollcommand=self.scrollbar.set)
        self.listbox.grid(row=0, column=0, sticky=tk.NSEW)

        # Configure the scrollbar to work with the listbox
        self.scrollbar.config(command=self.listbox.yview)

        # Configure grid weights to make the listbox expand with the window
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

    def insert_items(self, items):
        self.listbox.delete(0, tk.END)  # Clear existing items
        for item in items:
            self.listbox.insert(tk.END, item)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)

# Function to get file attributes
def get_file_attributes(path):
    items = []
    for entry in os.scandir(path):
        if entry.is_file():
            info = entry.stat()
            mod_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info.st_mtime))
            file_type = entry.name.split('.')[-1] if '.' in entry.name else 'Unknown'
            items.append((entry.name, info.st_size, mod_time, file_type))
    return items

def browse_directory():
    path = filedialog.askdirectory()
    if path:
        file_attributes = get_file_attributes(path)
        file_names = [f[0] for f in file_attributes]
        file_sizes = [f"{f[1]} bytes" for f in file_attributes]
        file_times = [f[2] for f in file_attributes]
        file_types = [f[3] for f in file_attributes]

        lb1.insert_items(file_names)
        lb2.insert_items(file_sizes)
        lb3.insert_items(file_times)
        lb4.insert_items(file_types)

# Create the main application window
root = tk.Tk()
root.title("Listbox with Scrollbar")

# Configure the main window's grid to expand with resizing
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)

# Create instances of the ScrollableListbox
lb1 = ScrollableListbox(root)
lb2 = ScrollableListbox(root)
lb3 = ScrollableListbox(root)
lb4 = ScrollableListbox(root)

# Place the listboxes in a grid
lb1.grid(row=1, column=1, sticky=tk.NSEW)
lb2.grid(row=1, column=2, sticky=tk.NSEW)
lb3.grid(row=1, column=3, sticky=tk.NSEW)
lb4.grid(row=1, column=4, sticky=tk.NSEW)

# Create and place the Browse button
browse_button = ttk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=0, column=0, pady=10)

# Run the application
root.mainloop()
