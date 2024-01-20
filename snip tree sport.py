import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tree = ttk.Treeview(self, columns=('Size', 'Modified'), show='headings')
        self.tree.heading('Size', text='Size')
        self.tree.heading('Modified', text='Modified')

        # Bind the column headers to the sorting function
        for col in ('Size', 'Modified'):
            self.tree.heading(col, text=col, command=lambda _col=col: self.treeview_sort_column(self.tree, _col, False))

        # Add some sample data
        data = [
            ("File1", 123, "2022-01-01"),
            ("File2", 456, "2022-01-02"),
            ("File3", 789, "2022-01-03"),
        ]
        for item in data:
            self.tree.insert('', 'end', values=item)

        self.tree.pack()


    def treeview_sort_column(self, tv, col, reverse):
        # Extract the data from the column and pair it with the row id
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        # Sort the list in the desired order (ascending or descending)
        l.sort(reverse=reverse)

        # Rearrange the items in the Treeview based on the sorted order
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # Toggle the sorting order for the next click
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

