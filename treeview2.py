import tkinter as tk
from tkinter import ttk, filedialog
import os

def load_file(event):
    selected = tree.focus()
    file_path = tree.item(selected, 'text')
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            text.delete('1.0', tk.END)
            text.insert(tk.END, file.read())

def populate_tree(tree, path):
    for p in os.listdir(path):
        abspath = os.path.join(path, p)
        oid = tree.insert('', tk.END, text=abspath, open=False)
        if os.path.isdir(abspath):
            populate_tree(tree, abspath)


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            text.delete('1.0', tk.END)
            text.insert(tk.END, file.read())

open_button = ttk.Button(root, text="Open File", command=open_file)
open_button.pack()

text = tk.Text(root, wrap='word')
text.pack(expand=True, fill='both')

root.mainloop()

root = tk.Tk()
root.title("File Viewer")

tree = ttk.Treeview(root)
tree.pack(side=tk.LEFT, fill=tk.Y)

text = tk.Text(root, wrap='word')
text.pack(side=tk.RIGHT, fill=tk.Y)

tree.bind('<<TreeviewSelect>>', load_file)

path = '.'  # Set the directory path you want to start with
populate_tree(tree, path)

root.mainloop()
