import tkinter as tk
from tkinter import filedialog
import os

def select_files():
    """ Open a dialog to select multiple files """
    file_paths = filedialog.askopenfilenames()
    file_list.delete(0, tk.END)
    for file_path in file_paths:
        file_list.insert(tk.END, file_path)

def add_character_and_rename():
    """ Add a character to each selected file and rename """
    char_to_add = character_entry.get()
    for file_path in file_list.get(0, tk.END):
        directory, filename = os.path.split(file_path)
        new_filename = char_to_add + filename
        new_filepath = os.path.join(directory, new_filename)
        os.rename(file_path, new_filepath)
    status_label.config(text="Files renamed successfully!")

# Create the main window
root = tk.Tk()
root.title("File Renamer")

# Create and pack widgets
select_button = tk.Button(root, text="Select Files", command=select_files)
select_button.pack()

file_list = tk.Listbox(root)
file_list.pack()

character_entry = tk.Entry(root)
character_entry.pack()

rename_button = tk.Button(root, text="Add Character and Rename", command=add_character_and_rename)
rename_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

# Run the application
root.mainloop()
