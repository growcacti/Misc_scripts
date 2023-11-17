import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.title("File Renamer")
root.geometry("400x300")  # Adjust size as needed
def enumerate_files(file_list):
    for index, file in enumerate(file_list):
        directory, filename = os.path.split(file)
        name, ext = os.path.splitext(filename)
        new_name = f"{name}_{index}{ext}"
        os.rename(file, os.path.join(directory, new_name))
def remove_spaces(file_list):
    for file in file_list:
        directory, filename = os.path.split(file)
        new_name = filename.replace(" ", "")
        os.rename(file, os.path.join(directory, new_name))
def add_suffix(file_list, suffix):
    for file in file_list:
        directory, filename = os.path.split(file)
        name, ext = os.path.splitext(filename)
        new_name = f"{name}{suffix}{ext}"
        os.rename(file, os.path.join(directory, new_name))
def select_files():
    file_paths = filedialog.askopenfilenames()
    return file_paths

btn_select = tk.Button(root, text="Select Files", command=select_files)
btn_select.pack()
btn_enumerate = tk.Button(root, text="Enumerate Files", command=lambda: enumerate_files(select_files()))
btn_enumerate.pack()

btn_remove_spaces = tk.Button(root, text="Remove Spaces", command=lambda: remove_spaces(select_files()))
btn_remove_spaces.pack()

entry_suffix = tk.Entry(root)
entry_suffix.pack()

btn_add_suffix = tk.Button(root, text="Add Suffix", command=lambda: add_suffix(select_files(), entry_suffix.get()))
btn_add_suffix.pack()
