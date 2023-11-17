import os
import tkinter as tk
from tkinter import filedialog

def list_files():
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_list.delete(0, tk.END)
        files = os.listdir(folder_path)
        for file in files:
            file_list.insert(tk.END, file)

def enumerate_files():
    new_names = []
    for index, item in enumerate(file_list.get(0, tk.END), start=1):
        _, ext = os.path.splitext(item)
        new_name = f"{index}{ext}"
        new_names.append(new_name)
    file_list.delete(0, tk.END)
    for new_name in new_names:
        file_list.insert(tk.END, new_name)

def remove_spaces():
    new_names = []
    for item in file_list.get(0, tk.END):
        new_name = item.replace(" ", "")
        new_names.append(new_name)
    file_list.delete(0, tk.END)
    for new_name in new_names:
        file_list.insert(tk.END, new_name)

def add_suffix():
    suffix = suffix_entry.get()
    if suffix:
        new_names = []
        for item in file_list.get(0, tk.END):
            _, ext = os.path.splitext(item)
            new_name = f"{item.split('.')[0]}_{suffix}{ext}"
            new_names.append(new_name)
        file_list.delete(0, tk.END)
        for new_name in new_names:
            file_list.insert(tk.END, new_name)

# Create the main application window
root = tk.Tk()
root.title("File Renamer")

# Create and configure widgets
list_button = tk.Button(root, text="List Files", command=list_files)
enumerate_button = tk.Button(root, text="Enumerate", command=enumerate_files)
remove_spaces_button = tk.Button(root, text="Remove Spaces", command=remove_spaces)
suffix_label = tk.Label(root, text="Suffix:")
suffix_entry = tk.Entry(root)
add_suffix_button = tk.Button(root, text="Add Suffix", command=add_suffix)
file_list = tk.Listbox(root, selectmode=tk.MULTIPLE)

# Grid layout
list_button.grid(row=0, column=0, padx=10, pady=10)
enumerate_button.grid(row=0, column=1, padx=10, pady=10)
remove_spaces_button.grid(row=0, column=2, padx=10, pady=10)
suffix_label.grid(row=1, column=0, padx=10, pady=10)
suffix_entry.grid(row=1, column=1, padx=10, pady=10)
add_suffix_button.grid(row=1, column=2, padx=10, pady=10)
file_list.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
