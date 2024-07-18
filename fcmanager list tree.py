import tkinter as tk
from tkinter import ttk
import os
import time

class FileManager:
    def __init__(self, root, directory='.'):
        self.directory = directory
        self.setup_widgets(root)
        self.populate_tree()

    def setup_widgets(self, root):
        container = ttk.Frame(root)
        container.pack(fill='both', expand=True)

        self.tree = ttk.Treeview(columns=('Name', 'Size', 'Date Modified', 'Type'), show='headings')
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.heading('Name', text='Name')
        self.tree.heading('Size', text='Size')
        self.tree.heading('Date Modified', text='Date Modified')
        self.tree.heading('Type', text='Type')
        
        self.tree.column('Name', width=200)
        self.tree.column('Size', width=100)
        self.tree.column('Date Modified', width=150)
        self.tree.column('Type', width=100)

        self.tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def populate_tree(self):
        for item in os.listdir(self.directory):
            filepath = os.path.join(self.directory, item)
            if os.path.isfile(filepath):
                item_type = 'File'
                item_size = os.path.getsize(filepath)
            elif os.path.isdir(filepath):
                item_type = 'Directory'
                item_size = '-'
            else:
                item_type = 'Unknown'
                item_size = '-'
                
            item_date = time.ctime(os.path.getmtime(filepath))
            
            self.tree.insert('', 'end', values=(item, item_size, item_date, item_type))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Manager")
    FileManager(root, directory='.')  # You can change the directory here
    root.mainloop()
