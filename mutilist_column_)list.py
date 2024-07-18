import tkinter as tk
from tkinter import ttk

class MultiColumnListbox:
    def __init__(self, root):
        self.setup_widgets(root)
        self.populate_data()

    def setup_widgets(self, root):
        container = ttk.Frame(root)
        container.pack(fill='both', expand=True)
        
        self.scrollbar = ttk.Scrollbar(container, orient="vertical")

        self.columns = ['Column1', 'Column2', 'Column3']
        self.listboxes = []

        for col in self.columns:
            frame = ttk.Frame(container)
            frame.pack(side="left", fill="both", expand=True)

            label = ttk.Label(frame, text=col)
            label.pack(side="top", fill="x")

            listbox = tk.Listbox(frame, exportselection=False, yscrollcommand=self.scrollbar.set)
            listbox.pack(side="top", fill="both", expand=True)
            self.listboxes.append(listbox)

        self.scrollbar.config(command=self.on_scroll)
        self.scrollbar.pack(side="right", fill="y")

    def on_scroll(self, *args):
        for listbox in self.listboxes:
            listbox.yview(*args)

    def populate_data(self):
        for i in range(100):
            self.listboxes[0].insert(tk.END, f'Item {i}')
            self.listboxes[1].insert(tk.END, f'Value {i}')
            self.listboxes[2].insert(tk.END, f'Other {i}')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Multi-Column Listbox with Synced Scrollbar")
    MultiColumnListbox(root)
    root.mainloop()
