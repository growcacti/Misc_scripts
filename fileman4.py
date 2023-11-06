import os
import tkinter as tk
from tkinter import ttk

class FileManager(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Simple File Manager')
        self.geometry('600x400')

        self.treeview = ttk.Treeview(self)
        self.treeview.pack(side='left', fill='both', expand=True)

        self.populate_root()

        self.treeview.bind('<<TreeviewOpen>>', self.expand_node)

    def populate_root(self):
        for drive in os.listdir('/'):
            self.insert_node('', drive, os.path.join('/', drive))

    def insert_node(self, parent, text, abspath):
        node = self.treeview.insert(parent, 'end', text=text, open=False)
        if os.path.isdir(abspath):
            # Insert a dummy child to make the item expandable
            self.treeview.insert(node, 'end')

    def expand_node(self, event):
        node = self.treeview.focus()
        abspath = self.get_node_abspath(node)

        # Prevent further expansion if the node is not a directory
        if not os.path.isdir(abspath):
            return

        # Clear dummy child and expand the directory
        self.treeview.delete(self.treeview.get_children(node))

        try:
            for entry in os.listdir(abspath):
                entry_path = os.path.join(abspath, entry)
                self.insert_node(node, entry, entry_path)
        except PermissionError:
            pass  # Ignore directories for which user has no access rights

    def get_node_abspath(self, node):
        path_parts = [self.treeview.item(node, 'text')]
        parent = self.treeview.parent(node)
        while parent:
            path_parts.append(self.treeview.item(parent, 'text'))
            parent = self.treeview.parent(parent)
        return os.path.join(*reversed(path_parts))


if __name__ == '__main__':
    file_manager = FileManager()
    file_manager.mainloop()
