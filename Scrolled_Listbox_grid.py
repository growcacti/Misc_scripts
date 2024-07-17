import tkinter as tk
from tkinter import ttk
import os

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
        for item in items:
            self.listbox.insert(tk.END, item)

# Create the main application window
root = tk.Tk()
root.title("Listbox with Scrollbar")

# Configure the main window's grid to expand with resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create an instance of the ScrollableListbox
scrollable_listbox = ScrollableListbox(root)

# Add some items to the listbox
items = [f"Item {i}" for i in range(100)]
scrollable_listbox.insert_items(items)

# Run the application
root.mainloop()
