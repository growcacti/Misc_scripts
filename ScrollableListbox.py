import tkinter as tk
from tkinter import ttk

class ScrollableListbox:
    def __init__(self, root):
        # Create a frame to contain the Listbox and Scrollbar
        self.frame = ttk.Frame(root)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the listbox and attach the scrollbar
        self.listbox = tk.Listbox(self.frame, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configure the scrollbar to work with the listbox
        self.scrollbar.config(command=self.listbox.yview)

    def insert_items(self, items):
        for item in items:
            self.listbox.insert(tk.END, item)

# Create the main application window
root = tk.Tk()
root.title("Listbox with Scrollbar")

# Create an instance of the ScrollableListbox
scrollable_listbox = ScrollableListbox(root)

# Add some items to the listbox
items = [f"Item {i}" for i in range(100)]
scrollable_listbox.insert_items(items)

# Run the application
root.mainloop()
