import tkinter as tk
from tkinter import filedialog, Listbox
import os
def add_prefix(files, prefix):
    for file in files:
        directory, filename = os.path.split(file)
        new_name = os.path.join(directory, prefix + filename)
        os.rename(file, new_name)

def insert_character(files, character):
    for file in files:
        directory, filename = os.path.split(file)
        name, ext = os.path.splitext(filename)
        new_name = os.path.join(directory, name + character + ext)
        os.rename(file, new_name)

def change_case(files, to_upper=True):
    for file in files:
        directory, filename = os.path.split(file)
        new_name = os.path.join(directory, filename.upper() if to_upper else filename.lower())
        os.rename(file, new_name)
root = tk.Tk()
root.title("File Renamer")

# Listbox for original file names
listbox_original = Listbox(root, height=15, width=50)
listbox_original.pack()

# Listbox for new file names
listbox_new = Listbox(root, height=15, width=50)
listbox_new.pack()


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


# Button to select files
btn_select = tk.Button(root, text="Select Files", command=select_files_and_update_list)
btn_select.pack()

# Additional widgets for prefix, suffix, and character insertion
entry_prefix = tk.Entry(root)
entry_prefix.pack()

entry_character = tk.Entry(root)
entry_character.pack()

# Buttons for new functions
btn_add_prefix = tk.Button(root, text="Add Prefix", command=lambda: add_prefix(select_files_and_update_list(), entry_prefix.get()))
btn_add_prefix.pack()

btn_insert_char = tk.Button(root, text="Insert Character", command=lambda: insert_character(select_files_and_update_list(), entry_character.get()))
btn_insert_char.pack()

# Existing buttons and entry widgets (enumerate, remove spaces, add suffix)
# ...

root.mainloop()
