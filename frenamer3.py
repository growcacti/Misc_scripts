import tkinter as tk
from tkinter import filedialog, Listbox
import os


def add_prefix(files, prefix):
    for file in files:
        dir_name, file_name = os.path.split(file)
        new_name = os.path.join(dir_name, f"{prefix}{file_name}")
        os.rename(file, new_name)

def insert_character(files, character):
    for file in files:
        dir_name, file_name = os.path.split(file)
        name, ext = os.path.splitext(file_name)
        new_name = os.path.join(dir_name, f"{name}{character}{ext}")
        os.rename(file, new_name)

def change_case(files, to_upper=True):
    for file in files:
        dir_name, file_name = os.path.split(file)
        new_file_name = file_name.upper() if to_upper else file_name.lower()
        new_name = os.path.join(dir_name, new_file_name)
        os.rename(file, new_name)
root = tk.Tk()
root.title("Advanced File Renamer")

selected_files = []

def update_listboxes():
    original_listbox.delete(0, tk.END)
    new_listbox.delete(0, tk.END)
    for file in selected_files:
        original_listbox.insert(tk.END, os.path.basename(file))
        # Simulate renaming for preview (without actually renaming)
        # You can modify this part to show the preview of new names based on selected operations
        new_listbox.insert(tk.END, "New_" + os.path.basename(file))

def on_file_select():
    global selected_files
    selected_files = list(select_files())
    update_listboxes()

# File selection and listboxes
btn_select = tk.Button(root, text="Select Files", command=on_file_select)
btn_select.pack()

original_listbox = Listbox(root)
original_listbox.pack()

new_listbox = Listbox(root)
new_listbox.pack()

# Entry and button for prefix
entry_prefix = tk.Entry(root)
entry_prefix.pack()
btn_add_prefix = tk.Button(root, text="Add Prefix", command=lambda: add_prefix(selected_files, entry_prefix.get()))
btn_add_prefix.pack()

# Entry and button for inserting characters
entry_character = tk.Entry(root)
entry_character.pack()
btn_insert_char = tk.Button(root, text="Insert Character", command=lambda: insert_character(selected_files, entry_character.get()))
btn_insert_char.pack()

# Other operations as before...

root.mainloop()
