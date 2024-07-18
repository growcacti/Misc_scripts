import tkinter as tk
from tkinter import ttk

class MultiColumnListbox:
    def __init__(self, root):
        self.setup_widgets(root)
        self.populate_data()

    def setup_widgets(self, root):
        container = ttk.Frame(root)
        container.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(container)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.columns = ['Column1', 'Column2', 'Column3']
        self.listboxes = {}

        for col in self.columns:
            frame = ttk.Frame(self.scrollable_frame)
            frame.pack(side="left", fill="y", expand=True)

            label = ttk.Label(frame, text=col)
            label.pack(side="top", fill="x")

            listbox = tk.Listbox(frame, exportselection=False)
            listbox.pack(side="top", fill="both", expand=True)
            self.listboxes[col] = listbox

    def populate_data(self):
        for i in range(100):
            self.listboxes['Column1'].insert(tk.END, f'Item {i}')
            self.listboxes['Column2'].insert(tk.END, f'Value {i}')
            self.listboxes['Column3'].insert(tk.END, f'Other {i}')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Multi-Column Listbox with Scrollbar")
    MultiColumnListbox(root)
    root.mainloop()
